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
"""

from __future__ import annotations

from typing import Any

from wahlwerk.vote.popular.popular_vote import PopularVote
from wahlwerk.vote.popular.tally import TallyKind
from wahlwerk_ui.sketch import guide
from wahlwerk_ui.sketch import primitives as sk
from wahlwerk_ui.sketch.plate import Plate
from wahlwerk_ui.style import FONT_SIZE_PX

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
    schematic panels elsewhere use general ones (region, district, unit).
    """
    rows = vote.tally.filter(unit=UNIT).rows
    plate = Plate("vote", "a popular vote, from the electorate to a tally")

    p = plate.panel(
        "electorate",
        "who votes",
        width=240,
        height=150,
        caption=("the electorate", "voters, each registered in", "one unit of one district"),
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
        sk.text(a, wk, 52, f"district {i + 1}", ink="plain")
        for j, x in enumerate((wk - 38, wk + 38)):
            sk.link(a, wk, 57, x, 76)
            sk.unit(a, x - 32, 78, 64, 86, f"unit {2 * i + j + 1}")
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
        sk.text(a, wk, 52, f"district {i + 1}")
        for x in xs[2 * i : 2 * i + 2]:
            sk.link(a, wk, 57, x, 80)
            sk.dot(a, x, 86, 6, cls="subject")
    sk.unit(a, 96, 102, 108, 50, "municipality")
    sk.axis(a, 110, 92, 110, 102)
    sk.axis(a, 190, 92, 190, 102)
    sk.text(a, 150, 166, "administrative, beside the ids", ink="faint")
    return plate


def build_sketches(vote: PopularVote) -> dict[str, Any]:
    """Every plate of the site, as the page reads them."""
    return {
        "key": KEY,
        "unit": UNIT,
        "plates": {
            plate.name: plate.to_dict()
            for plate in (vote_plate(vote), who_plate(), what_plate(), recorded_plate(vote))
        },
        "style": [plate.to_dict() for plate in guide.plates()],
    }
