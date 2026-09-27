"""Data build: derive each election with the engine, emit clean JSON for the frontend.

Run from the repository root, with wahlwerk-data cloned beside it:

    uv run python build.py [--data ../wahlwerk-data]

Writes ``docs/data/elections.json``. Every number in it is derived by the engine from
the votes in wahlwerk-data under the law in force on election day; nothing is copied
from an official result. The page shows these numbers and never computes seats itself.
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

logger = logging.getLogger("build")

HERE = Path(__file__).parent
OUT = HERE / "docs" / "data" / "elections.json"
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
    args = parser.parse_args()
    data_dir: Path = args.data
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parties = PartyRegistry.from_json(data_dir / PARTIES)
    payload = {
        "engine": version("wahlwerk"),
        "elections": [
            build_election(key, body, day, data_dir, parties)
            for key, body, day in ELECTIONS
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    logger.info("wrote %s", OUT.relative_to(HERE))


if __name__ == "__main__":
    main()
