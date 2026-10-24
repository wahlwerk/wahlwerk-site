"""The Law pages' content, read from the engine: each law's protocol, its structure, its
drawing, and every kind of step it is made of.

Nothing about a law is typed into the site. The steps, their settings and the paragraph
each follows are the engine's law objects (``wahlwerk.law``); the stages, what each step
reads from which, and where each step could move without changing the result come from
``wahlwerk.process.allocation.flow``, derived from what the steps read and write; the
drawing is wahlwerk-ui's ``plot.protocol``; what a kind of step does is the first
paragraph of its docstring (read like the formulas, :func:`formulas.segments`). Beside
each top-level step of the drawing stands the chamber as one election's run had decided
it after that step (:func:`asides`), from the engine's own allocation.
"""

from __future__ import annotations

import inspect
from typing import Any

from wahlwerk.law.base import Law
from wahlwerk.process.allocation import flow
from wahlwerk.process.allocation.base import Allocation, AllocationStep, check_protocol
from wahlwerk.vote.popular.popular_vote import PopularVote
from wahlwerk_ui.plot.protocol import aside_svg, margin_of, protocol_svg

from formulas import segments

__all__ = ["build_laws"]

SHORT: dict[str, str] = {"de.st.lwg.2021": "LWG LSA", "de.mv.lkwg.2011": "LKWG M-V"}
"""The abbreviation a law is cited with, by law id; the engine's Law has no field yet."""


def build_laws(laws: list[Law], replays: dict[str, tuple[str, PopularVote]] | None = None) -> dict[str, Any]:
    """``laws.json``: each law with its steps and drawing, then every kind of step.
    ``replays`` gives per law id the election (its key and vote) whose chamber the
    drawing shows beside each step."""
    kinds: dict[str, dict[str, Any]] = {}
    out = []
    for law in laws:
        protocol = law.protocol
        steps = flow.protocol_data(protocol)
        for position, step in enumerate(steps):
            span = flow.movable(protocol, position)
            step["movable"] = [span.start, span.stop - 1]
        replay = (replays or {}).get(law.id)
        out.append(
            {
                "id": law.id,
                "short": SHORT.get(law.id, law.id),
                "title": law.title,
                "citation": law.citation,
                "source": law.source,
                "body": law.body,
                "steps": steps,
                "facts": _facts(steps),
                "parts": _parts(steps, law, replay[1] if replay else None),
                "replay": replay[0] if replay else None,
            }
        )
        for path, step in _every(protocol):
            _note_kind(kinds, step, law, path)
    return {"laws": out, "kinds": sorted(kinds.values(), key=lambda k: k["order"])}


def _every(protocol: tuple[AllocationStep, ...], prefix: tuple[Any, ...] = ()) -> list[tuple[tuple[Any, ...], AllocationStep]]:
    from wahlwerk.law.edit import steps

    return [((*prefix, *path), step) for path, step in steps(protocol)]


def _note_kind(kinds: dict[str, dict[str, Any]], step: AllocationStep, law: Law, path: tuple[Any, ...]) -> None:
    cls = type(step)
    entry = kinds.setdefault(
        cls.__name__,
        {
            "kind": cls.__name__,
            "qualname": f"{cls.__module__}.{cls.__qualname__}",
            "summary": segments(" ".join((inspect.getdoc(cls) or "").split("\n\n")[0].split())),
            "inputs": [list(pair) for pair in step.inputs.items()],
            "reads": sorted(step.reads),
            "writes": sorted(step.writes),
            "holds": any(isinstance(getattr(step, f), tuple) and getattr(step, f) and isinstance(getattr(step, f)[0], AllocationStep) for f in cls.model_fields),
            "uses": [],
            "computes": [],
            "order": len(kinds),
        },
    )
    for use in flow.uses(step):
        concept = use.model_dump(mode="json")
        if concept not in entry["computes"]:
            entry["computes"].append(concept)
    entry["uses"].append({"law": law.id, "short": SHORT.get(law.id, law.id), "citation": step.citation, "path": list(path)})


def _facts(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Each fact of the allocation this protocol builds: which steps write it and which
    read it, top-level steps only (a loop counts for what it holds)."""
    facts: dict[str, dict[str, Any]] = {"tally": {"fact": "tally", "written": ["the vote"], "read": []}}
    for position, step in enumerate(steps):
        name = f"{position + 1} {step['kind']}"
        for fact in step["writes"]:
            facts.setdefault(fact, {"fact": fact, "written": [], "read": []})["written"].append(name)
        for fact in [*step["reads"], *step["optional_reads"]]:
            facts.setdefault(fact, {"fact": fact, "written": [], "read": []})["read"].append(name)
    return list(facts.values())


STEP_WIDTH = 640
"""The width a step is drawn at, as the whole drawing was: scaled to the page's column,
with its chamber in the margin beside it where the window has room."""

CHAMBER_WIDTH = 176
"""The width of the chamber beside each step."""


def _parts(steps: list[dict[str, Any]], law: Law, vote: PopularVote | None) -> list[dict[str, Any]]:
    """The drawing in parts, one per top-level step, each with the chamber after it: the
    steps share the facts' column, so they line up when set one under the other."""
    margin = margin_of(steps, STEP_WIDTH)
    order, chambers = asides(vote, law) if vote is not None else ([], [None] * len(steps))
    return [
        {
            "drawing": str(protocol_svg([step], width=STEP_WIDTH, margin=margin)),
            "chamber": str(aside_svg(chamber, width=CHAMBER_WIDTH, labels=order)) if chamber else None,
        }
        for step, chamber in zip(steps, chambers)
    ]


def asides(vote: PopularVote, law: Law) -> tuple[list[str | None], list[dict[str, Any]]]:
    """The chamber after each top-level step of ``law`` on ``vote`` (wahlwerk-ui's
    asides), and the parties in the order of the chamber formed at the end, largest first:
    the engine applies the steps, this only says what each result shows.

    After the chamber is formed every seat is filled. Before, with an entitlement, each
    party has as many seats as it is entitled to, filled as far as its unit winners fill
    them and open for its list; unit winners beyond that stand without a seat (the
    overhang). With only the units decided, their winners are seated and the rest of
    the chamber size is free; before that the whole chamber is free.
    """
    check_protocol(law.protocol)
    results = []
    allocation = Allocation(tally=vote.tally)
    for step in law.protocol:
        allocation = step.apply(allocation)
        results.append(allocation)
    final = results[-1].chamber
    order = [p for p, _ in sorted((final.seats_by_party if final else {}).items(), key=lambda kv: (kv[0] is None, -kv[1]))]
    return order, [_aside(result, order) for result in results]


def _aside(allocation: Allocation, order: list[str | None]) -> dict[str, Any]:
    size = allocation.chamber_size or 0
    if allocation.chamber is not None:
        held = allocation.chamber.seats_by_party
        seats = [[p, held[p], 0] for p in order if held.get(p)]
        return {"seats": seats, "free": 0, "standing": [], "caption": "all filled"}
    if allocation.unit_mandates is None:
        return {"seats": [], "free": size, "standing": [], "caption": "none filled" if size else ""}
    wins: dict[str | None, int] = dict(allocation.unit_wins())
    independent = sum(1 for d in allocation.unit_mandates if d.party is None)
    if independent:
        wins[None] = independent
    due = dict(allocation.entitlement.seats) if allocation.entitlement is not None else {}
    if None in wins:
        due[None] = wins[None]
    if not due:
        seats = [[p, wins[p], 0] for p in order if wins.get(p)]
        filled = sum(wins.values())
        return {"seats": seats, "free": max(size - filled, 0), "standing": [], "caption": f"{filled} filled"}
    seats = [[p, min(due.get(p, 0), wins.get(p, 0)), due.get(p, 0) - min(due.get(p, 0), wins.get(p, 0))] for p in order if due.get(p)]
    standing = [[p, wins.get(p, 0) - due.get(p, 0)] for p in order if wins.get(p, 0) > due.get(p, 0)]
    filled = sum(s[1] for s in seats)
    return {
        "seats": seats,
        "free": max(size - sum(due.values()), 0),
        "standing": standing,
        "caption": f"{filled} filled",
    }
