"""The formulas of the site, read from wahlwerk.calc: written once, in its docstrings.

Each module of ``wahlwerk.calc`` documents its formulas in its docstrings (reST, with
``:math:`` and ``.. math::`` for the formulas and ``:cite:`` for the literature); the
API reference renders them with Sphinx, and this module reads the same docstrings into
``docs/data/formulas.json`` for the Formulas page, which renders the math with KaTeX.
So a formula is written once and reads the same in the code, the reference and here,
with the symbols of ``wahlwerk.calc.notation``.

The reader knows the few reST forms the docstrings use (paragraphs, ``.. math::``
blocks, simple tables, and the roles ``math``, ``cite``, ``func``, ``class``, ``mod``,
``data`` and double backquotes) and nothing else; doctest examples are left out.
"""

from __future__ import annotations

import importlib
import importlib.metadata
import inspect
import re
from typing import Any

import wahlwerk.calc
from wahlwerk.calc.notation import SYMBOLS

__all__ = ["build_formulas", "segments"]

ROLE = re.compile(
    r":(math|cite|func|class|mod|data|meth|attr):`([^`]+)`|``([^`]+)``|\*\*([^*]+)\*\*"
)


def segments(text: str) -> list[dict[str, Any]]:
    """Running text as segments: ``text``, ``strong``, ``math`` (LaTeX), ``code`` and
    ``cite`` (a list of BibTeX keys)."""
    text = " ".join(text.split())
    out: list[dict[str, Any]] = []
    at = 0
    for match in ROLE.finditer(text):
        if match.start() > at:
            out.append({"text": text[at : match.start()]})
        role, value, literal, strong = match.groups()
        if strong is not None:
            out.append({"strong": strong})
        elif literal is not None:
            out.append({"code": literal})
        elif role == "math":
            out.append({"math": value})
        elif role == "cite":
            out.append({"cite": [key.strip() for key in value.split(",")]})
        else:
            name = value.lstrip("~").split(".")[-1].rstrip("()")
            out.append({"code": name + ("()" if role in ("func", "meth") else "")})
        at = match.end()
    if at < len(text):
        out.append({"text": text[at:]})
    return out


def _blocks(doc: str) -> list[dict[str, Any]]:
    """A docstring as paragraphs, display formulas and tables; doctests left out."""
    lines = inspect.cleandoc(doc).splitlines()
    blocks: list[dict[str, Any]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith(">>>"):
            while i < len(lines) and lines[i].strip():
                i += 1
            continue
        if line.startswith(".. math::"):
            i += 1
            body: list[str] = []
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith("   ")):
                body.append(lines[i].strip())
                i += 1
            blocks.append({"math": " ".join(part for part in body if part)})
            continue
        if re.fullmatch(r"=+( +=+)+", line.strip()):
            table, i = _table(lines, i)
            blocks.append(table)
            continue
        if line.startswith(".. "):  # another directive: skip it with its body
            i += 1
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith("   ")):
                i += 1
            continue
        paragraph = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(".. "):
            paragraph.append(lines[i])
            i += 1
        text = " ".join(paragraph)
        if text.startswith("- "):
            blocks.append({"list": [segments(item) for item in re.split(r"(?:^| )- ", text) if item.strip()]})
        else:
            blocks.append({"p": segments(text)})
    return blocks


def _table(lines: list[str], i: int) -> tuple[dict[str, Any], int]:
    """A reST simple table: head row, rule, body rows, closing rule."""
    border = lines[i]
    spans = [(m.start(), m.end()) for m in re.finditer(r"=+", border)]

    def cells(row: str) -> list[list[dict[str, Any]]]:
        out = []
        for n, (start, end) in enumerate(spans):
            stop = spans[n + 1][0] if n + 1 < len(spans) else len(row)
            out.append(segments(row[start:stop].strip()))
        return out

    head = cells(lines[i + 1])
    rows = []
    i += 3
    while i < len(lines) and lines[i].strip() != border.strip():
        if lines[i].strip():
            rows.append(cells(lines[i]))
        i += 1
    return {"table": {"head": head, "rows": rows}}, i + 1


def _cites(blocks: list[dict[str, Any]]) -> list[str]:
    found: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key in value.get("cite", []):
                if key not in found:
                    found.append(key)
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(blocks)
    return found


def _module(name: str) -> dict[str, Any]:
    module = importlib.import_module(f"wahlwerk.calc.{name}")
    blocks = _blocks(module.__doc__ or "")
    title = blocks.pop(0)["p"] if blocks and "p" in blocks[0] else []
    functions = []
    for item in getattr(module, "__all__", []):
        obj = getattr(module, item)
        if not (inspect.isfunction(obj) or inspect.isclass(obj)) or not obj.__doc__:
            continue
        doc = _blocks(obj.__doc__)
        summary = doc[0]["p"] if doc and "p" in doc[0] else []
        functions.append(
            {
                "name": item,
                "qualname": f"wahlwerk.calc.{name}.{item}",
                "kind": "class" if inspect.isclass(obj) else "function",
                "summary": summary,
            }
        )
    every = [*blocks, *(f["summary"] for f in functions)]
    return {
        "name": name,
        "qualname": f"wahlwerk.calc.{name}",
        "title": title,
        "body": blocks,
        "functions": functions,
        "cites": _cites(every),
    }


def build_formulas() -> dict[str, Any]:
    """``formulas.json``: the symbols, then every module of wahlwerk.calc by layer."""
    return {
        "calc": importlib.metadata.version("wahlwerk"),
        "symbols": [
            {"latex": s.latex, "meaning": s.meaning, "group": s.group} for s in SYMBOLS
        ],
        "layers": [
            {"title": title, "modules": [_module(name) for name in names]}
            for title, names in wahlwerk.calc.LAYERS
        ],
    }
