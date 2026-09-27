# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`wahlwerk-site` is the website of the wahlwerk project: it explains each component of the
engine (vote, law as protocol, allocation, chamber) so anyone can follow it, using real
elections the engine reproduces exactly. It is one of six sibling repositories:

```
CODE/wahlwerk_/
  wahlwerk/                  the engine       Apache-2.0
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
build.py                  <- data build: engine + wahlwerk-data in, docs/data/elections.json out
docs/                     <- GitHub Pages root, committed
  data/elections.json     <- written by build.py only
  index.html, assets/     <- written by npm run build only
  favicon.svg, .nojekyll  <- hand-written
frontend/src/
  main.ts                 <- installs the tokens, mounts App
  app.css                 <- global element styles; colours and fonts via var(--...)
  App.svelte              <- loads elections.json, lays out the sections
  components/
    Pieces.svelte         <- the four roles (input, protocol, process, state) and the modules
    Protocol.svelte       <- the LWG LSA as the engine's protocol (law/de/st/lwg.py)
    Results.svelte        <- election tabs, seat grid, result table, note, source
    SeatGrid.svelte       <- one square per seat: solid Wahlkreis, outlined list
    Hierarchies.svelte    <- unit ids and the administrative tree
    ThemeToggle.svelte    <- auto / light / dark
  lib/
    tokens.ts             <- DESIGN TOKENS: every colour (light and dark), party colour, font
    types.ts              <- the shape of elections.json
    elections.ts          <- per-election labels and notes (prose only)
```

## Rules

- **Every number on the page comes from the engine.** Seats, votes and shares are derived by
  `build.py` through `wahlwerk`; the frontend never computes seats and never hard-codes a
  result. Prose (`lib/elections.ts`, the sections) may state facts the engine derives, but a
  count that the page can show from `elections.json` is shown from there.
- **Only golden elections.** `ELECTIONS` in `build.py` lists elections whose official result
  the engine's golden tests reproduce. Add one only when its golden test exists.
- **Protocol text follows the engine.** Step names and fields in `Protocol.svelte` copy
  `law/de/st/lwg.py`; when the engine renames a step, update the page.
- **Tokens only.** No component hard-codes a colour, font or radius; add a token to
  `lib/tokens.ts` with a `usage` note. Party colours encode parties in data and nothing else.
- **Both themes.** Every colour token has a light and a dark value; check both.
- **Phone width.** The page works at 390 px with a 16 px gutter and no sideways page scroll;
  wide tables scroll inside `.table-wrap`.
- **Sources are named.** Every result shows its publisher, title, licence and attribution
  from the bundle's `[source]`.
- **Language:** English prose, German terms of art (`Wahlkreis`, `Zweitstimme`, `Überhang`),
  the same policy as the engine's README.
- No em-dashes in any text.
