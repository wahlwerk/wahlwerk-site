"""The references of the site, from their three homes.

- **Literature** (books, papers, judgments): the engine's ``docs/references.bib``,
  exported from Zotero (Better BibLaTeX). Cited with a number; the same file feeds the
  API reference (sphinxcontrib-bibtex).
- **Statutes**: the engine's law registry, one entry per version (``Law.id``, the
  citation of its Fassung, its source, the dates it was in force), so a citation names
  the version it means. A statute the page cites but the engine does not implement
  (the Grundgesetz, the GO-BT) is in :data:`CITED_STATUTES` until the engine records it.
  Cited inline in the German form, with the section: ``Art. 63 GG``.
- **Data**: each bundle's ``[source]``, as the engine reads it.

``build.py`` writes the three to ``docs/data/references.json``; the page formats them
(``lib/citations.ts``). The BibTeX reader is small, not an implementation of BibTeX: it
keeps the fields a reference shows and drops the rest (abstracts, file paths).
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from wahlwerk.law.base import Law
from wahlwerk.vote.popular.popular_vote import PopularVote

__all__ = ["CITED_STATUTES", "KEEP", "build_references", "parse_bibtex", "read_bibtex"]

KEEP = (
    "author",
    "title",
    "shorttitle",
    "journaltitle",
    "journal",
    "shortjournal",
    "booktitle",
    "publisher",
    "location",
    "volume",
    "number",
    "pages",
    "date",
    "year",
    "note",
    "doi",
    "url",
    "urldate",
)
"""The BibTeX fields a reference on the page shows; everything else stays in Zotero."""

SHORT: dict[str, str] = {"de.st.lwg.2021": "LWG LSA", "de.mv.lkwg.2011": "LKWG M-V"}
"""The abbreviation a law is cited with, by law id; the engine's Law has no field yet."""

CITED_STATUTES: dict[str, dict[str, Any]] = {
    "de.bund.gg": {
        "short": "GG",
        "title": "Grundgesetz für die Bundesrepublik Deutschland",
        "citation": "cited in the version in force today",
        "source": "https://www.gesetze-im-internet.de/gg/",
        "implemented": False,
    },
    "de.bund.gobt": {
        "short": "GO-BT",
        "title": "Geschäftsordnung des Deutschen Bundestages",
        "citation": "cited in the version in force today; Sec. 10 (1) is the engine's caucus protocol (wahlwerk.law.de.bund.gobt)",
        "source": "https://www.gesetze-im-internet.de/btgo_1980/",
        "implemented": False,
    },
}
"""Statutes the site cites that the engine does not record as a ``Law`` yet."""

_ENTRY = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)
_FIELD = re.compile(r"\s*(\w+)\s*=\s*")


def _value(text: str, start: int) -> tuple[str, int]:
    """A braced or quoted field value starting at ``start``; returns it and the end."""
    opener = text[start]
    if opener == "{":
        depth, i = 0, start
        while i < len(text):
            if text[i] == "{" and text[i - 1] != "\\":
                depth += 1
            elif text[i] == "}" and text[i - 1] != "\\":
                depth -= 1
                if depth == 0:
                    return text[start + 1 : i], i + 1
            i += 1
        raise ValueError(f"unbalanced braces at {start}")
    if opener == '"':
        end = text.index('"', start + 1)
        return text[start + 1 : end], end + 1
    match = re.match(r"[^,}\s]+", text[start:])
    if not match:
        raise ValueError(f"no value at {start}")
    return match.group(0), start + match.end()


def parse_bibtex(text: str) -> dict[str, dict[str, str]]:
    """Entries by key: ``{"type": ..., field: value}`` for the fields in :data:`KEEP`."""
    entries: dict[str, dict[str, str]] = {}
    for match in _ENTRY.finditer(text):
        kind, key = match.group(1).lower(), match.group(2)
        if kind in ("comment", "string", "preamble"):
            continue
        if key in entries:
            raise ValueError(f"duplicate BibTeX key {key!r}")
        record = {"type": kind}
        i = match.end()
        while field := _FIELD.match(text, i):
            value, i = _value(text, field.end())
            if field.group(1).lower() in KEEP:
                record[field.group(1).lower()] = " ".join(value.split())
            comma = re.match(r"\s*,", text[i:])
            if comma:
                i += comma.end()
        entries[key] = record
    return entries


def read_bibtex(path: Path) -> dict[str, dict[str, str]]:
    """The literature in ``path``, or none if the file is not there yet."""
    return parse_bibtex(path.read_text(encoding="utf-8")) if path.exists() else {}


def _statute(law: Law) -> dict[str, Any]:
    return {
        "short": SHORT.get(law.id, law.id),
        "title": law.title,
        "citation": law.citation,
        "source": law.source,
        "in_force_from": law.in_force_from.isoformat() if law.in_force_from else None,
        "in_force_until": law.in_force_until.isoformat() if law.in_force_until else None,
        "implemented": True,
    }


def build_references(
    bib: Path, laws: Iterable[Law], votes: dict[str, PopularVote]
) -> dict[str, Any]:
    """Literature, statutes and data sources, as ``references.json``."""
    statutes: dict[str, dict[str, Any]] = {str(law.id): _statute(law) for law in laws}
    statutes.update(CITED_STATUTES)
    return {
        "literature": read_bibtex(bib),
        "statutes": statutes,
        "data": {
            key: {
                "publisher": vote.source.publisher,
                "title": vote.source.title,
                "url": vote.source.url,
                "licence": vote.source.licence,
                "attribution": vote.source.attribution,
            }
            for key, vote in votes.items()
        },
    }
