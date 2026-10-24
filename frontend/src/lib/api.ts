/**
 * Links from a concept on this site to its entry in the engine's API reference
 * (Sphinx, built from the wahlwerk repository) and to its source on GitHub.
 *
 * The site explains; the reference documents every field and parameter. A page links
 * a concept to the reference rather than copying any of it, so the two cannot drift.
 */

export const API_BASE = 'https://wahlwerk.github.io/wahlwerk';
export const SOURCE_BASE = 'https://github.com/wahlwerk/wahlwerk/blob/main/src';

/** The API page of each top-level module or package (wahlwerk/docs/api/<page>.md). */
const PAGES: Record<string, string> = {
  model: 'foundation',
  ids: 'foundation',
  log: 'foundation',
  party: 'party',
  state: 'state',
  vote: 'vote',
  apportionment: 'apportionment',
  process: 'process',
  law: 'law',
  calc: 'calc',
  io: 'io',
};

/** "wahlwerk.vote.popular.tally.TallyRow" -> its anchor in the API reference. */
export function apiHref(qualname: string): string {
  const page = PAGES[qualname.split('.')[1]] ?? 'index';
  return `${API_BASE}/api/${page}.html#${qualname}`;
}

/** The source file an object is defined in. Objects are named by their full path. */
export function sourceHref(qualname: string): string {
  const parts = qualname.split('.');
  return `${SOURCE_BASE}/${parts.slice(0, -1).join('/')}.py`;
}

/** The short name shown on the page. */
export function shortName(qualname: string): string {
  return qualname.split('.').pop() ?? qualname;
}
