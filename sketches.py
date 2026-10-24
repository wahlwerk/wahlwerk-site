"""The sketches of the Vote page, drawn with wahlwerk-ui from a real popular vote.

Every number in a sketch is read through the engine from the bundle it names; the
drawings are schematic, the numbers are not. ``build.py`` writes them, panel by panel,
to ``docs/data/sketches.json``, together with the style guide plates of wahlwerk-ui.

The plates, in the order the page shows them:

- ``vote``: from the electorate to a tally, the four steps of a popular vote
- ``who``: who votes; the electorate or the members of a body
- ``what``: what is voted on, by anyone; a list, a person, an option, several marks,
  x out of y, an order: examples, not a closed list
- ``recorded``: what a tally records; one row, the kinds, the two hierarchies

and, for the home page, ``home``: the whole path in four panels, the electorate, the
tally, the allocation a law describes as steps, and the chamber, each box a link to
the page that explains it (``links``, in the coordinates of the panel's art).
"""

from __future__ import annotations

from typing import Any

from wahlwerk.law.base import Law
from wahlwerk.process.allocation.allocate import allocate, derive
from wahlwerk.process.allocation.base import Allocation
from wahlwerk.process.allocation.overhang import (
    RaiseByOverhang,
    RaiseChamberSize,
    RaiseUntilBalanced,
)
from wahlwerk.vote.popular.popular_vote import PopularVote
from wahlwerk.vote.popular.tally import TallyKind
from wahlwerk_ui.plot.chamber.common import party_tones
from wahlwerk_ui.plot.chamber.seat import seat_layout
from wahlwerk_ui.sketch import guide
from wahlwerk_ui.sketch import primitives as sk
from wahlwerk_ui.sketch.plate import Plate
from wahlwerk_ui.style import CHAR_WIDTH_PX, FONT_SIZE_PX

KEY = "de.landtag.st.2026"
"""The bundle the numbers come from."""

UNIT = "de.st.wk.001.gem.15081026.wbz.000001"
"""The Wahlbezirk the tally sketches show."""

FIELDS = ("unit", "level", "kind", "section", "channel", "party", "candidate", "option", "count")


def _short(unit: str) -> str:
    """A unit id short enough for a panel: its first and last segments."""
    parts = unit.split(".")
    return ".".join(parts[:4]) + "…" + ".".join(parts[-2:]) if len(parts) > 6 else unit


def vote_plate(vote: PopularVote) -> Plate:
    """A popular vote in four steps: electorate, ballot paper, counting, tally.

    The panels that show data use the example's own unit names (wahlkreis, wbz); the
    schematic panels elsewhere use general ones (a region and the units under it).
    """
    rows = vote.tally.filter(unit=UNIT).rows
    plate = Plate("vote", "a popular vote, from the electorate to a tally")

    p = plate.panel(
        "electorate",
        "who votes",
        width=240,
        height=150,
        caption=("the electorate", "voters, each registered in", "one unit of the lowest level"),
    )
    a = p.art
    sk.unit(a, 1, 1, 238, 148, "wahlkreis 001")
    for i, n in enumerate((16, 12, 14)):
        x = 10 + i * 56
        sk.unit(a, x, 24, 50, 112, f"wbz {i + 1}")
        sk.crowd(a, x + 4, 40, 42, 90, n)
    sk.unit(a, 180, 24, 52, 112, "brief")
    sk.crowd(a, 184, 40, 44, 90, 7, cls="hollow", r=2.2)

    p = plate.panel(
        "ballot",
        "what each voter does",
        width=220,
        height=150,
        caption=("the ballot paper", "two sections, one mark each:", "a person and a list"),
    )
    sk.ballot_paper(
        p.art,
        1,
        20,
        218,
        [
            ("erststimme", ["person a", "person b", "person c"], 0),
            ("zweitstimme", ["afd", "cdu", "linke", "spd"], 1),
        ],
    )

    p = plate.panel(
        "counting",
        "how it is counted",
        width=220,
        height=150,
        caption=("counted per unit", "at the polling station, and", "by post in a unit of its own"),
    )
    a = p.art
    sk.box(a, 10, 26, 52, 40)  # the urn
    a.line("structure", 28, 26, 44, 26)  # its slot, drawn as a gap in the lid
    sk.text(a, 36, 50, "urne", ink="faint")
    sk.box(a, 10, 92, 52, 34)  # the envelope
    a.add("structure", "path", {"class": "structure", "d": "M10,92 L36,112 L62,92"})
    sk.text(a, 36, 140, "brief", ink="faint")
    sk.box(a, 130, 40, 80, 76)
    sk.text(a, 170, 66, "count", ink="strong", is_name=True)
    sk.text(a, 170, 82, "per unit,", ink="faint")
    sk.text(a, 170, 96, "per section", ink="faint")
    sk.arrow(a, 66, 46, 126, 66)
    sk.arrow(a, 66, 109, 126, 92)

    p = plate.panel(
        "tally",
        "what is recorded",
        width=300,
        height=170,
        caption=("the tally", "one row per count; valid", "totals are sums, not stored"),
    )
    a = p.art
    sk.text(a, 1, FONT_SIZE_PX, _short(UNIT), ink="faint", anchor="start")
    shown = [r for r in rows if r.kind is not TallyKind.VOTES]
    shown += [r for r in rows if r.kind is TallyKind.VOTES and r.section == "zweitstimme"][:3]
    table_rows = [
        (
            r.kind.value,
            r.section or "",
            r.channel or "",
            r.party or "",
            str(r.count),
        )
        for r in shown
    ]
    sk.table(
        a,
        1,
        FONT_SIZE_PX + 6,
        ("kind", "section", "channel", "party", "count"),
        table_rows,
        numeric=(False, False, False, False, True),
    )
    return plate


def who_plate() -> Plate:
    """Who votes: the electorate, counted per unit; the members of a body, per mandate. The
    chamber vote is drawn on a motion (yes, no, abstain), one of the things it can be on."""
    plate = Plate("who", "who votes")
    p = plate.panel(
        "popular",
        "popular vote",
        width=300,
        height=170,
        caption=("the electorate", "anonymous and secret, counted", "per unit, summed up the tree"),
    )
    a = p.art
    sk.text(a, 150, 14, "region", ink="strong", is_name=True)
    for i, wk in enumerate((75, 225)):
        sk.link(a, 150, 19, wk, 40)
        sk.text(a, wk, 52, f"unit {i + 1}", ink="plain")
        for j, x in enumerate((wk - 38, wk + 38)):
            sk.link(a, wk, 57, x, 76)
            sk.unit(a, x - 32, 78, 64, 86, f"unit {i + 1}.{j + 1}")
            sk.crowd(a, x - 28, 96, 56, 64, 12 + 3 * j)

    p = plate.panel(
        "chamber",
        "chamber vote",
        width=300,
        height=170,
        caption=(
            "the members of a body",
            "one ballot per mandate, on",
            "anything; here a motion",
        ),
    )
    a = p.art
    choices = ["yes"] * 9 + ["no"] * 6 + ["abstain"] * 2 + ["yes"] * 4 + ["absent"] + ["no"] * 3
    seats = sk.chamber(a, 150, 150, 110, choices)
    sk.leader(a, 40, 24, seats[3][0], seats[3][1])
    sk.text(a, 38, 20, "mandate 4: yes", anchor="start")
    sk.leader(a, 262, 24, seats[21][0], seats[21][1])
    sk.text(a, 262, 20, "absent", ink="faint", anchor="end")
    sk.text(a, 150, 140, f"{len(choices)} mandates", ink="faint")
    return plate


def what_plate() -> Plate:
    """What is voted on, in a popular or a chamber vote: six forms a choice takes. Examples,
    not a closed list; the engine limits neither kind of vote to any of them."""
    plate = Plate("what", "what is voted on")
    w, h = 170, 120

    p = plate.panel(
        "list",
        "a list",
        width=w,
        height=h,
        caption=("a party list", "one mark,", "counted per party"),
    )
    sk.ballot_paper(p.art, 1, 10, 168, [("zweitstimme", ["afd", "cdu", "linke", "spd"], 2)])

    p = plate.panel(
        "person",
        "a person",
        width=w,
        height=h,
        caption=("a person", "one mark,", "counted per candidate"),
    )
    sk.ballot_paper(p.art, 1, 10, 168, [("erststimme", ["a · afd", "b · cdu", "c · spd"], 1)])

    p = plate.panel(
        "option",
        "yes or no",
        width=w,
        height=h,
        caption=("an option", "yes, no, sometimes more:", "a referendum, a motion"),
    )
    sk.ballot_paper(p.art, 1, 10, 168, [("volksentscheid", ["ja", "nein"], 0)])

    p = plate.panel(
        "several",
        "several marks",
        width=w,
        height=h,
        caption=("several marks", "more than one per person,", "or across lists"),
    )
    a = p.art
    sk.box(a, 1, 10, 168, 100)
    sk.text(a, 85, 10 + FONT_SIZE_PX + 3, "up to 3 per person", ink="faint")
    for j, (name, crossed) in enumerate(
        (("a1 · list a", 2), ("a2 · list a", 0), ("b1 · list b", 1))
    ):
        y = 44 + j * 22
        sk.text(a, 8, y + 4, name, anchor="start")
        for k in range(3):
            sk.mark(a, 108 + k * 18, y, is_marked=k < crossed)

    p = plate.panel(
        "select",
        "x out of y",
        width=w,
        height=h,
        caption=("x out of y", "choose up to x options,", "one count each"),
    )
    a = p.art
    sk.box(a, 1, 10, 168, 100)
    sk.text(a, 85, 10 + FONT_SIZE_PX + 3, "choose up to 2", ink="faint")
    for j, (name, marked) in enumerate(
        (("person a", True), ("person b", False), ("person c", True), ("person d", False))
    ):
        y = 40 + j * 17
        sk.mark(a, 16, y, is_marked=marked)
        sk.text(a, 28, y + 4, name, anchor="start")

    p = plate.panel(
        "order",
        "an order",
        width=w,
        height=h,
        caption=("a ranking", "one count per order:", "not modelled yet"),
    )
    a = p.art
    sk.box(a, 1, 10, 168, 100)
    sk.text(a, 85, 10 + FONT_SIZE_PX + 3, "rank them", ink="faint")
    for j, (name, rank) in enumerate((("person a", "2"), ("person b", "1"), ("person c", "3"))):
        y = 44 + j * 22
        sk.box(a, 12, y - 8, 16, 16, cls="hollow")
        sk.text(a, 20, y + 4, rank, ink="strong", is_name=True)
        sk.text(a, 36, y + 4, name, anchor="start")
    return plate


def recorded_plate(vote: PopularVote) -> Plate:
    """What a tally records: one row, the kinds per Wahlbezirk, the two hierarchies."""
    tally = vote.tally.filter(unit=UNIT)
    rows = tally.rows
    plate = Plate("recorded", "what a tally records")

    row = next(r for r in rows if r.kind is TallyKind.VOTES and r.section == "zweitstimme")
    p = plate.panel(
        "row",
        "one row",
        width=250,
        height=170,
        caption=("one tally row", "nine fields; blank is absent,", "never zero"),
    )
    a = p.art
    for i, field in enumerate(FIELDS):
        y = 14 + i * 17
        value = getattr(row, field)
        value = value.value if isinstance(value, TallyKind) else value
        sk.text(a, 70, y, field, ink="faint", anchor="end")
        if value is None:
            sk.unit(a, 78, y - 10, 60, 13)
            sk.text(a, 145, y, "absent", ink="faint", anchor="start")
        else:
            text = _short(str(value)) if field == "unit" else str(value)
            sk.text(a, 78, y, text, ink="strong" if field == "count" else "plain", anchor="start")

    def total(kind: TallyKind, **criteria: Any) -> int:
        return sum(r.count for r in tally.filter(kind=kind, **criteria).rows)

    eligible = total(TallyKind.ELIGIBLE)
    voters = total(TallyKind.VOTERS)
    invalid = total(TallyKind.INVALID, section="zweitstimme")
    valid = total(TallyKind.VOTES, section="zweitstimme")
    p = plate.panel(
        "kinds",
        "the kinds",
        width=280,
        height=170,
        caption=("per unit", "eligible, voters, invalid and", "votes; valid is a sum"),
    )
    a = p.art
    full = 260

    def bar(y: float, count: int, cls: str, label: str) -> None:
        width = full * count / eligible
        sk.box(a, 10, y, width, 16, cls=cls, rx=1)
        sk.text(a, 10, y - 4, label, ink="faint", anchor="start")
        sk.text(a, 10 + width - 3, y + 12, str(count), ink="strong", anchor="end")

    bar(20, eligible, "paper", "eligible")
    bar(60, voters, "subject", "voters")
    bar(100, valid, "subject", "votes, zweitstimme (sum)")
    sk.box(a, 10 + full * valid / eligible, 100, full * invalid / eligible, 16, cls="neutral", rx=0)
    sk.text(
        a,
        10 + full * (valid + invalid) / eligible + 4,
        112,
        f"+{invalid} invalid",
        ink="faint",
        anchor="start",
    )
    sk.dimension(
        a, 10, 140, 10 + full * voters / eligible, 140, f"turnout {100 * voters / eligible:.0f} %"
    )

    p = plate.panel(
        "hierarchies",
        "two hierarchies",
        width=300,
        height=170,
        caption=(
            "two hierarchies",
            "the law counts along one;",
            "an administrative unit crosses it",
        ),
    )
    a = p.art
    sk.text(a, 150, 14, "region", ink="strong", is_name=True)
    xs = (40, 110, 190, 260)
    for i, wk in enumerate((75, 225)):
        sk.link(a, 150, 19, wk, 40)
        sk.text(a, wk, 52, f"unit {i + 1}")
        for x in xs[2 * i : 2 * i + 2]:
            sk.link(a, wk, 57, x, 80)
            sk.dot(a, x, 86, 6, cls="subject")
    sk.unit(a, 96, 102, 108, 50, "municipality")
    sk.axis(a, 110, 92, 110, 102)
    sk.axis(a, 190, 92, 190, 102)
    sk.text(a, 150, 166, "administrative, beside the ids", ink="faint")
    return plate


Link = dict[str, Any]
"""A clickable region of a panel: ``href``, ``label`` and ``x``, ``y``, ``w``, ``h`` in px of its art."""


def _link(href: str, label: str, x: float, y: float, w: float, h: float) -> Link:
    return {"href": href, "label": label, "x": x, "y": y, "w": w, "h": h}


def home_plate(vote: PopularVote, law: Law) -> tuple[Plate, dict[str, list[Link]]]:
    """From the people to a chamber, in four panels, every box a link.

    The tally shows the vote's own Land totals; the allocation lists the law's own
    steps; the chamber is what the engine derives from that vote under that law.
    """
    plate = Plate("home", "from the electorate to a chamber")
    links: dict[str, list[Link]] = {}
    height = 196

    p = plate.panel("electorate", "the electorate", width=150, height=height,
                    caption=("who votes", "each voter, in one unit"))
    a = p.art
    sk.unit(a, 1, 1, 148, height - 2, "the people")
    sk.crowd(a, 10, 26, 130, height - 40, 46)
    links["electorate"] = [_link("#/vote", "the vote: who votes and how", 0, 0, 150, height)]

    p = plate.panel("tally", "the tally", width=190, height=height,
                    caption=("what is recorded", "votes per unit, summed up"))
    a = p.art
    land = vote.tally.sum_to("land").filter(kind=TallyKind.VOTES, section="zweitstimme")
    totals = sorted(land.sum_by("party").items(), key=lambda kv: -kv[1])
    rows = [(str(party), f"{count:,}".replace(",", " ")) for party, count in totals[:6]]
    rows.append(("…", ""))
    sk.box(a, 1, 1, 188, height - 2)
    sk.text(a, 10, FONT_SIZE_PX + 8, "zweitstimme, land", ink="faint", anchor="start")
    sk.table(a, 10, FONT_SIZE_PX + 18, ("party", "votes"), rows, numeric=(False, True))
    links["tally"] = [_link("#/vote", "the tally a vote leaves", 0, 0, 190, height)]

    steps = law.protocol
    width = 300
    p = plate.panel("allocation", "the allocation", width=width, height=height,
                    caption=("what the law does", "a list of steps, one record"))
    a = p.art
    sk.unit(a, 1, 1, width - 2, height - 2, law.id)
    top, gap = 24.0, 4.0
    step_h = (height - top - 8 - gap * (len(steps) - 1)) / len(steps)
    step_links = []
    for i, step in enumerate(steps):
        y = top + i * (step_h + gap)
        name = getattr(step, "title", None) or type(step).__name__  # a sequence by its title
        sk.box(a, 10, y, width - 20, step_h)
        sk.text(a, 18, y + step_h / 2 + FONT_SIZE_PX / 2 - 2, name, ink="strong", is_name=True, anchor="start")
        if step.citation and (len(name) + len(step.citation) + 3) * CHAR_WIDTH_PX < width - 36:
            sk.text(a, width - 18, y + step_h / 2 + FONT_SIZE_PX / 2 - 2, step.citation.lower(), ink="faint", anchor="end")
        step_links.append(_link("#/law/steps", f"step {i + 1}: {name}", 10, y, width - 20, step_h))
    links["allocation"] = [_link("#/law/allocation", "the allocation", 0, 0, width, top), *step_links]

    chamber = allocate(vote, steps)
    seats = sorted(chamber.seats_by_party.items(), key=lambda kv: -kv[1])
    p = plate.panel("chamber", "the chamber", width=200, height=height,
                    caption=(f"{chamber.size} seats", "derived from these votes"))
    a = p.art
    groups = [(party, count) for party, count in seats]
    centres, seat_r = seat_layout(chamber.size)
    radius, cx, floor = 92.0, 100.0, height - 40
    scale = radius / (1 + seat_r)
    seat = 0
    for (_, count), (key, colour) in zip(groups, party_tones(groups, None)):
        a.parties.setdefault(key, colour)
        for x, y in centres[seat : seat + count]:
            sk.dot(a, cx + x * scale, floor - y * scale, seat_r * scale * 0.92, cls=f"party-{key}")
        seat += count
    a.line("structure", 4, floor + seat_r * scale + 3, 196, floor + seat_r * scale + 3)
    links["chamber"] = [_link("#/chamber", "the chamber, seat by seat", 0, 0, 200, height)]
    return plate, links


OVERHANG: dict[str, str] = {"de.st.lwg.2021": "de.landtag.st.2021", "de.mv.lkwg.2011": "de.landtag.mv.2021"}
"""Per law, the election its overhang plate replays: the one whose chamber grew most
(Sachsen-Anhalt 2021: 83 to 97 seats; Mecklenburg-Vorpommern 2021: 71 to 79)."""

LOOPS = (RaiseByOverhang, RaiseUntilBalanced)


def overhang_plate(vote: PopularVote, law: Law) -> Plate:
    """The law's overhang loop round by round, from the engine's own rounds, each round a
    half circle of the chamber at that size.

    One panel per run of the repeated block that changes something: the first, each one
    where the overhang changes, and the last. The chamber has as many seats as its size,
    each party as many as it is entitled to: solid where a unit winner of the party
    fills it, open (its colour as the edge) where a list seat is still to fill. A party
    that won more units than its seats has members with no seat yet: they stand below
    the floor, the overhang, until the chamber is raised enough to seat them.
    """
    at = next(i for i, step in enumerate(law.protocol) if isinstance(step, LOOPS))
    loop = law.protocol[at]
    assert isinstance(loop, LOOPS)
    every = loop.rounds(derive(vote, law.protocol[:at]))

    def excess(result: Allocation) -> int:
        return sum(n for _, n in result.overhang or ())

    shown = [r for i, r in enumerate(every) if i in (0, len(every) - 1) or excess(r) != excess(every[i - 1])]
    first = every[0]
    assert first.entitlement is not None
    parties = [p for p, _ in sorted(first.entitlement.seats, key=lambda kv: -kv[1])]
    tones = dict(party_tones([(p, 1) for p in parties], None))
    plate = Plate(f"overhang-{law.id}", "raising the chamber size for overhang")
    width, radius = 240.0, 108.0
    cx, floor = width / 2, 4 + radius
    for number, result in enumerate(shown, start=1):
        assert result.entitlement is not None
        entitled = dict(result.entitlement.seats)
        wins = result.unit_wins()
        size = result.chamber_size or 0
        later = every[every.index(result) + 1 :]
        if excess(result) and isinstance(loop, RaiseByOverhang):
            # The factor is the round's own first step's: RaiseChamberSize.
            factor = next(s.increment.factor for s in loop.protocol if isinstance(s, RaiseChamberSize))
            note = (f"overhang {excess(result)}: next", f"{size} + {factor} × {excess(result)} = {size + factor * excess(result)}")
        elif excess(result):
            steps = next((i + 1 for i, r in enumerate(later) if excess(r) != excess(result)), len(later))
            note = (f"overhang {excess(result)}: a seat", f"at a time, {steps} more")
        elif later:
            note = (f"balanced at {size}, even:", "one seat more")
        else:
            note = ("every member seated:", "done")
        p = plate.panel(f"round-{number}", f"{size} seats", width=width, height=floor + 34, caption=(f"round {every.index(result) + 1}", *note))
        a = p.art
        for key in parties:
            a.parties.setdefault(key, tones[key])
        # Seats left to right, party by party: its unit winners first, then its open list seats.
        kinds: list[str] = []
        for party in parties:
            due, won_n = entitled.get(party, 0), wins.get(party, 0)
            kinds += [f"party-{party}"] * min(due, won_n) + [f"party-{party}-open"] * (due - min(due, won_n))
        centres, seat_r = seat_layout(len(kinds))
        scale = radius / (1 + seat_r)
        for (x, y), cls in zip(centres, kinds):
            sk.dot(a, cx + x * scale, floor - y * scale, seat_r * scale * 0.85, cls=cls)
        a.line("structure", 4, floor + seat_r * scale + 2, width - 4, floor + seat_r * scale + 2)
        sk.text(a, cx, floor - 6, str(size), ink="strong", is_name=True)
        # Members without a seat: the overhang, standing below the floor.
        standing = [(party, wins.get(party, 0) - entitled.get(party, 0)) for party in parties]
        standing = [(party, n) for party, n in standing if n > 0]
        x = 10.0
        r = seat_r * scale * 0.85
        for party, n in standing:
            for _ in range(n):
                sk.dot(a, x, floor + 18, r, cls=f"party-{party}")
                x += 2.6 * r
            sk.text(a, x + 2, floor + 22, f"{party} +{n}: no seat yet", ink="plain", anchor="start")
            x += 120
    return plate


def build_sketches(
    vote: PopularVote,
    law: Law,
    home_vote: PopularVote | None = None,
    overhang: list[tuple[PopularVote, Law]] | None = None,
) -> dict[str, Any]:
    """Every plate of the site, as the page reads them. ``home_vote`` (the vote the home
    plate's numbers come from) is ``vote`` unless given; ``overhang`` holds the vote and
    law of each overhang plate (:data:`OVERHANG`)."""
    home, links = home_plate(home_vote or vote, law)
    home_dict = home.to_dict()
    for panel in home_dict["panels"]:
        panel["links"] = links.get(panel["name"], [])
    return {
        "key": KEY,
        "unit": UNIT,
        "plates": {
            plate.name: plate.to_dict()
            for plate in (vote_plate(vote), who_plate(), what_plate(), recorded_plate(vote))
        }
        | {"home": home_dict}
        | {plate.name: plate.to_dict() for plate in (overhang_plate(v, law) for v, law in overhang or ())},
        "style": [plate.to_dict() for plate in guide.plates()],
    }
