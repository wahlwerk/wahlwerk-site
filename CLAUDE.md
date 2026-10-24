# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`wahlwerk-site` is the website of the wahlwerk project: it explains each component of the
engine (vote, law as protocol, allocation, chamber, and the formulas under them) so anyone can follow it, using real
elections the engine reproduces exactly. It is one of six sibling repositories:

```
CODE/wahlwerk_/
  wahlwerk/                  the engine       GPL-3.0
  wahlwerk-data/             the archive      GPL-3.0; data: its source's licence
  wahlwerk-data-processing/  bundle makers
  wahlwerk-execute/          notebooks
  wahlwerk-ui/               charts (optional extra of the engine)
  wahlwerk-site/             the website      GPL-3.0        <- you are here
```

The dependency runs one way: the site depends on the engine and the archive, never the
reverse. Modelling logic belongs in the engine; the site only calls it and shows the result.

The project is built **step by step**. Do only the step asked for; do not add pages,
sections or features ahead of it.

## Commands

```sh
uv sync                                  # Python env; the engine from ../wahlwerk (editable)
uv run python build.py                   # derive the elections -> docs/data/elections.json
uv run python build.py --data <path>     # wahlwerk-data elsewhere than ../wahlwerk-data
uv run ruff check build.py

cd frontend
npm install
npm run dev                              # serves docs/ as public dir, so data/ resolves
npm run check                            # svelte-check, must report 0 errors and 0 warnings
npm run build                            # docs/index.html + docs/assets/
```

`uv run mypy --strict build.py` fails on the engine's imports until the engine ships a
`py.typed` marker.

`npm run build` does not empty `docs/` (it would delete `docs/data/`), so old hashed files
stay in `docs/assets/`; delete the stale ones before committing.

## Architecture

```
build.py                  <- data build: engine + wahlwerk-data in, docs/data/*.json out
sketches.py               <- the Vote page's sketch plates, drawn with wahlwerk-ui from a real bundle
references.py             <- sources from their three homes: references.bib, the law registry, bundles
formulas.py               <- the Formulas page's content, read from wahlwerk-calc's docstrings
docs/                     <- GitHub Pages root, committed
  data/elections.json     <- written by build.py only
  data/sketches.json      <- written by build.py only: one SVG per panel, plus wahlwerk-ui's style plates
  data/references.json    <- written by build.py only: literature, statutes, data
  data/formulas.json      <- written by build.py only: wahlwerk-calc's symbols, formulas, tables, citations
  index.html, assets/     <- written by npm run build only
  favicon.svg, .nojekyll  <- hand-written
frontend/src/
  main.ts                 <- installs the tokens, mounts App
  app.css                 <- global element styles; colours and fonts via var(--...)
  App.svelte              <- loads the data, follows the hash route (a #place link scrolls and
                             keeps the route), top bar, side panel, footer
  components/
    Sidebar.svelte        <- the side panel, as in IR-bands: the pages on top, the outline of the
                             page shown below (its h2/h3, read from the page, the one being read
                             marked); docked from 1080 px, a drawer behind the menu button below
    Home.svelte           <- hero, live stats, one card per component
    Icon.svelte           <- one symbol per component, in currentColor
    Vote.svelte           <- Vote page: a vote, who votes, what is voted on, what is recorded
    Hierarchies.svelte    <- Vote page, last section: unit ids and the administrative tree
    Plate.svelte          <- a sketch plate: numbered panels that wrap at phone width
    CodeRef.svelte        <- "in the code": links into the API reference and the source
    Law.svelte            <- a statute cited inline (Art. 63 GG), linked to its version
    Term.svelte           <- a term of art (Landtag): italic, dotted underline, concept on hover
    Cite.svelte           <- a literature citation, a superscript number
    RefList.svelte        <- a page's sources: literature, statutes, data
    Protocol.svelte       <- Law page: the LWG LSA as the engine's protocol (law/de/st/lwg.py)
    Pieces.svelte         <- Allocation page: the four roles and the modules
    Formulas.svelte       <- Formulas page: every formula of wahlwerk-calc by layer, the notation, the literature
    Segments.svelte       <- docstring text from formulas.json: inline math, code, citations, terms of art
    Math.svelte           <- one formula in LaTeX, rendered by KaTeX
    Results.svelte        <- Chamber page: election tabs, seat grid, result table, note, source
    SeatGrid.svelte       <- one square per seat: solid Wahlkreis, outlined list
    Impressum.svelte      <- § 5 DDG, sources and licences, privacy, disclaimer
    StyleGuide.svelte     <- every token, read from tokens.ts, and the rules
    ThemeToggle.svelte    <- auto / light / dark
  lib/
    tokens.ts             <- DESIGN TOKENS: every colour (light and dark), party colour, font
    pages.ts              <- the pages, hash routes (#/vote ...) and the five components in order
    impressum.ts          <- the operator's name, address and contact for the Impressum
    types.ts              <- the shape of elections.json
    elections.ts          <- per-election labels and notes (prose only)
    citations.ts          <- formats literature, statutes and data sources
    glossary.ts           <- every term of art: the concept it instantiates, its system, a gloss
    api.ts                <- links to the API reference (wahlwerk.github.io/wahlwerk) and to the source
```

## Rules

- **Every number on the page comes from the engine.** Seats, votes and shares are derived by
  `build.py` through `wahlwerk`; the frontend never computes seats and never hard-codes a
  result. Prose (`lib/elections.ts`, the sections) may state facts the engine derives, but a
  count that the page can show from `elections.json` is shown from there.
- **Only golden elections.** `ELECTIONS` in `build.py` lists elections whose official result
  the engine's golden tests reproduce. Add one only when its golden test exists.
- **Formulas are written once, in wahlwerk-calc.** The Formulas page shows the LaTeX,
  prose and tables of `wahlwerk_calc`'s docstrings (`formulas.py`), with the symbols of
  `wahlwerk_calc.notation`; it never types a formula itself. A formula wrong on the page is
  fixed in the docstring, which fixes the API reference too.
- **Protocol text follows the engine.** Step names and fields in `Protocol.svelte` copy
  `law/de/st/lwg.py`; when the engine renames a step, update the page.
- **Tokens only.** No component hard-codes a colour, font or radius; add a token to
  `lib/tokens.ts` with a `usage` note. Party colours encode parties in data and nothing else.
- **Both themes.** Every colour token has a light and a dark value; check both.
- **One column, one measure.** A content page is one column, `--page-width`; text,
  drawings, tables and sources all span it, so every left and right edge is the same.
  Running prose (a section's paragraphs and plain lists, `.prose`) is justified with
  hyphenation, list markers hang outside the column; below 600 px prose is ragged and
  markers sit inside. No component sets its own `max-width` on prose.
- **The side panel** holds the site's pages and the page's outline, nothing else for now.
  The outline is read from the page's headings, so a heading is the outline entry; a
  heading that should not be listed sits inside `data-outline="skip"`.
- **Phone width.** The page works at 390 px with a 16 px gutter and no sideways page scroll;
  wide tables scroll inside `.table-wrap`.
- **Sources are named.** Every result shows its publisher, title, licence and attribution
  from the bundle's `[source]`.
- **Language:** English prose, German terms of art (`Wahlkreis`, `Zweitstimme`, `Überhang`),
  the same policy as the engine's README.
- **Sketches are drawn in code**, by `sketches.py` with wahlwerk-ui, never by hand and never
  in a component: the drawing may be schematic, every number in it comes from the engine.
  The style is wahlwerk-ui's `STYLE.md`.
- **The site explains, the reference documents.** A concept links to its API entry
  (`CodeRef`), it never copies a field list or a signature.
- **Every claim has a source**, from its own home: literature numbered from the engine's
  `docs/references.bib` (Zotero), statutes inline in their own form (`Art. 63 GG`) linked to
  the version in the engine's law registry, data named with publisher, licence and
  attribution. A statute the engine does not implement goes in the engine's
  `docs/statutes.toml`, which the API reference reads too.
- **Concepts first, systems as examples.** Write about what holds in any system, in plain
  words, and use one system as the worked example. Four roles of text: a concept plain
  (bold where defined); a term of art, the name one system gives a concept, through
  `<Term t="Landtag" />` (italic, dotted underline, its concept on hover), every one in
  `lib/glossary.ts`; code in monospace, linked by `CodeRef`; a statute through `<Law>`.
  The style guide's Writing section shows them.
- No em-dashes in any text.
