# wahlwerk-site

The website of [wahlwerk](https://github.com/wahlwerk/wahlwerk): the engine's components
explained step by step, with real elections the engine reproduces exactly.

## Build

With `wahlwerk` and `wahlwerk-data` cloned beside this repository:

```sh
uv sync                        # Python environment, the engine installed from ../wahlwerk
uv run python build.py         # derive the elections, write docs/data/elections.json

cd frontend
npm install
npm run dev                    # local server, serves docs/ as the public directory
npm run build                  # writes docs/index.html and docs/assets/
```

`docs/` is committed and served by GitHub Pages (branch `main`, folder `/docs`).

## Licence

The site's code is GPL-3.0. The election data shown on it comes from wahlwerk-data and is
under its source's licence, which the page names with each result.
