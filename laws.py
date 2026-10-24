"""The Law pages' content, read from the engine: each law's protocol, its structure, its
drawing, and every kind of step it is made of.

Nothing about a law is typed into the site. The steps, their settings and the paragraph
each follows are the engine's law objects (``wahlwerk.law``); the stages, what each step
reads from which, and where each step could move without changing the result come from
``wahlwerk.process.allocation.flow``, derived from what the steps read and write; the
drawing is wahlwerk-ui's ``plot.protocol``; what a kind of step does is the first
paragraph of its docstring (read like the formulas, :func:`formulas.segments`).
"""

from __future__ import annotations

import inspect
from typing import Any

from wahlwerk.law.base import Law
from wahlwerk.process.allocation import flow
from wahlwerk.process.allocation.base import AllocationStep
from wahlwerk_ui.plot.protocol import protocol_svg

from formulas import segments

__all__ = ["build_laws"]

SHORT: dict[str, str] = {"de.st.lwg.2021": "LWG LSA", "de.mv.lkwg.2011": "LKWG M-V"}
"""The abbreviation a law is cited with, by law id; the engine's Law has no field yet."""


def build_laws(laws: list[Law]) -> dict[str, Any]:
    """``laws.json``: each law with its steps and drawing, then every kind of step."""
    kinds: dict[str, dict[str, Any]] = {}
    out = []
    for law in laws:
        protocol = law.protocol
        steps = flow.protocol_data(protocol)
        for position, step in enumerate(steps):
            span = flow.movable(protocol, position)
            step["movable"] = [span.start, span.stop - 1]
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
                "drawing": str(protocol_svg(steps, width=640, title=law.title)),
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
            "reads": sorted(step.reads),
            "writes": sorted(step.writes),
            "holds": any(isinstance(getattr(step, f), tuple) and getattr(step, f) and isinstance(getattr(step, f)[0], AllocationStep) for f in cls.model_fields),
            "uses": [],
            "order": len(kinds),
        },
    )
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
