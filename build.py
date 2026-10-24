"""Data build: derive each election with the engine, emit clean JSON for the frontend.

Run from the repository root, with wahlwerk-data cloned beside it:

    uv run python build.py [--data ../wahlwerk-data]

Writes three files to ``docs/data/``:

- ``elections.json``: every number derived by the engine from the votes in wahlwerk-data
  under the law in force on election day; nothing is copied from an official result.
  The page shows these numbers and never computes seats itself.
- ``sketches.json``: the sketches of the Vote page and the home page's path from the
  electorate to a chamber (``sketches.py``), drawn with
  wahlwerk-ui from a real bundle, one SVG per panel, and wahlwerk-ui's style guide.
- ``references.json``: the sources, from their three homes (``references.py``): the
  engine's ``docs/references.bib`` (Zotero) and ``docs/statutes.toml``, its law
  registry, the bundles; the same sources as the engine's API reference.
- ``laws.json``: each law's protocol with its stages, where each step could move, the
  facts it builds and its drawing, then every kind of step (``laws.py``), all from the
  engine's law objects.
- ``formulas.json``: the formulas of wahlwerk.calc with their symbols, prose, tables
  and citations, read from its docstrings (``formulas.py``), the same text the API
  reference renders.
"""

from __future__ import annotations

import argparse
import json
import logging
from datetime import date
from importlib.metadata import version
from pathlib import Path
from typing import Any

from wahlwerk.law.registry import LAWS
from wahlwerk.party.registry import PartyRegistry
from wahlwerk.process.allocation.allocate import derive
from wahlwerk.vote.popular.popular_vote import PopularVote

from formulas import build_formulas
from laws import build_laws
from references import build_references
from sketches import KEY as SKETCH_KEY
from sketches import build_sketches

logger = logging.getLogger("build")

HERE = Path(__file__).parent
DATA = HERE / "docs" / "data"
OUT = DATA / "elections.json"
PARTIES = Path("parties") / "de" / "de.bund.json"

# The elections the page shows: bundle key, body, election day. Only elections whose
# result the engine reproduces exactly (its golden tests) belong here.
ELECTIONS: tuple[tuple[str, str, date], ...] = (
    ("de.landtag.st.2026", "de.st.landtag", date(2026, 9, 6)),
    ("de.landtag.st.2021", "de.st.landtag", date(2021, 6, 6)),
    ("de.landtag.mv.2021", "de.mv.landtag", date(2021, 9, 26)),
    ("de.landtag.mv.2016", "de.mv.landtag", date(2016, 9, 4)),
    ("de.landtag.mv.2011", "de.mv.landtag", date(2011, 9, 4)),
)

SECTION = "zweitstimme"
LEVEL = "land"


def build_election(
    key: str, body: str, day: date, data_dir: Path, parties: PartyRegistry
) -> dict[str, Any]:
    """One election as the page reads it: the law, the source, and per party the
    Zweitstimmen and the seats, split into Wahlkreis and list seats."""
    vote = PopularVote.from_key(key, data_dir)
    law = LAWS.in_force(body, day)
    allocation = derive(vote, law.protocol)
    chamber = allocation.chamber
    if chamber is None:
        raise ValueError(f"{key}: {law.id} formed no chamber")

    votes = allocation.votes_by_party(LEVEL, SECTION)
    seats: dict[str, int] = {}
    wahlkreis: dict[str, int] = {}
    for mandate in chamber.mandates:
        if mandate.party is None:
            raise ValueError(f"{key}: mandate {mandate.id} has no party")
        seats[mandate.party] = seats.get(mandate.party, 0) + 1
        if mandate.id.startswith("wk."):
            wahlkreis[mandate.party] = wahlkreis.get(mandate.party, 0) + 1

    rows = []
    for party_id in sorted(seats, key=lambda p: (-seats[p], -votes.get(p, 0), p)):
        party = parties.get(party_id)
        rows.append(
            {
                "id": party_id,
                "name": party.name if party else party_id,
                "short_name": party.short_name if party else party_id,
                "votes": votes.get(party_id, 0),
                "seats": seats[party_id],
                "wahlkreis": wahlkreis.get(party_id, 0),
                "list": seats[party_id] - wahlkreis.get(party_id, 0),
            }
        )

    source = vote.source
    logger.info("%s: %d seats under %s", key, chamber.size, law.id)
    return {
        "key": key,
        "body": body,
        "date": day.isoformat(),
        "law": {"id": law.id, "title": law.title, "citation": law.citation},
        "source": {
            "publisher": source.publisher,
            "title": source.title,
            "url": source.url,
            "licence": source.licence,
            "attribution": source.attribution,
        },
        "seats": chamber.size,
        "valid_votes": sum(votes.values()),
        "parties": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--data",
        type=Path,
        default=HERE.parent / "wahlwerk-data",
        help="the wahlwerk-data checkout (default: beside this repository)",
    )
    parser.add_argument(
        "--engine",
        type=Path,
        default=HERE.parent / "wahlwerk",
        help="the wahlwerk checkout, for docs/references.bib and docs/statutes.toml "
        "(default: beside this repository)",
    )
    args = parser.parse_args()
    data_dir: Path = args.data
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parties = PartyRegistry.from_json(data_dir / PARTIES)
    payload = {
        "engine": version("wahlwerk"),
        "elections": [
            build_election(key, body, day, data_dir, parties) for key, body, day in ELECTIONS
        ],
    }
    write(OUT, payload)

    sketch_vote = PopularVote.from_key(SKETCH_KEY, data_dir)
    sketch_law = next(LAWS.in_force(body, day) for key, body, day in ELECTIONS if key == SKETCH_KEY)
    write(DATA / "sketches.json", build_sketches(sketch_vote, sketch_law))
    write(
        DATA / "references.json",
        build_references(
            args.engine / "docs" / "references.bib",
            args.engine / "docs" / "statutes.toml",
            LAWS.laws,
            {SKETCH_KEY: sketch_vote},
        ),
    )
    write(DATA / "formulas.json", build_formulas())
    shown = [LAWS.in_force(body, day) for _, body, day in ELECTIONS]
    write(DATA / "laws.json", build_laws(list({law.id: law for law in shown}.values())))


def write(path: Path, payload: object) -> None:
    """Write ``payload`` as JSON, the way every file in docs/data/ is written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    logger.info("wrote %s", path.relative_to(HERE))


if __name__ == "__main__":
    main()
