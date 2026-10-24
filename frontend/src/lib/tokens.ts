/**
 * Design tokens: the single source of truth for every colour, typeface and
 * layout constant on the site.
 *
 * Rules of the road:
 *   1. No component hard-codes a colour, font or size. Use the CSS custom
 *      property a token emits (var(--ink), var(--serif), ...).
 *   2. Every colour has a light and a dark value. `installTokens()` (called
 *      from main.ts) writes both into one stylesheet: light on :root, dark
 *      under prefers-color-scheme and under [data-theme="dark"], so the
 *      theme toggle overrides the system setting either way.
 *   3. Adding a token means adding it here with a `usage` note.
 *
 * The palette and type come from the design note "Tally to Landtag": warm
 * paper, near-black ink, one gold accent, Literata for headings, IBM Plex
 * for text and code.
 */

export interface ColorToken {
  light: string;
  dark: string;
  usage: string;
}

export const COLORS: Record<string, ColorToken> = {
  bg:            { light: '#f6f5f1', dark: '#15161a', usage: 'Page background' },
  surface:       { light: '#ffffff', dark: '#1d1f24', usage: 'Cards, nodes, protocol steps' },
  ink:           { light: '#1d1f24', dark: '#e9e7e1', usage: 'Body text and headings' },
  muted:         { light: '#5d606a', dark: '#a3a5ad', usage: 'Secondary text, table headers' },
  line:          { light: '#dcd9d0', dark: '#34363d', usage: 'Borders and rules' },
  accent:        { light: '#b8860b', dark: '#e0b54a', usage: 'Eyebrows, legal citations, the process node, focus' },
  'accent-soft': { light: '#f3e7c4', dark: '#3a3222', usage: 'Badges and active controls' },
  'code-bg':     { light: '#efede6', dark: '#23252b', usage: 'Inline code and code blocks' },
  shadow:        { light: 'rgba(29, 31, 36, 0.10)', dark: 'rgba(0, 0, 0, 0.45)', usage: 'Lift of a hovered card' },
};

/**
 * Party colours, keyed by the party id the engine uses. Only for encoding a
 * party in data (seats, swatches); never for chrome. A party missing here
 * falls back to `party-other`.
 */
export const PARTY_COLORS: Record<string, ColorToken> = {
  // Copied from wahlwerk-ui's src/wahlwerk_ui/parties.py: change them there first.
  afd:          { light: '#0a8fcf', dark: '#3aa9e0', usage: 'AfD' },
  bsw:          { light: '#6d2a55', dark: '#b0619a', usage: 'BSW' },
  cdu:          { light: '#2a2c31', dark: '#c9c7c0', usage: 'CDU' },
  'cdu-csu':    { light: '#2a2c31', dark: '#c9c7c0', usage: 'CDU/CSU, the caucus' },
  csu:          { light: '#0080c8', dark: '#3a9ee0', usage: 'CSU' },
  fdp:          { light: '#d9a800', dark: '#f0c93a', usage: 'FDP' },
  fw:           { light: '#e58a00', dark: '#f5ab40', usage: 'Freie Wähler' },
  gruene:       { light: '#3e8a25', dark: '#62b046', usage: 'BÜNDNIS 90/DIE GRÜNEN' },
  linke:        { light: '#b3276d', dark: '#dc5a98', usage: 'Die Linke' },
  npd:          { light: '#7a4a1f', dark: '#b07a48', usage: 'NPD' },
  pds:          { light: '#b3276d', dark: '#dc5a98', usage: 'PDS' },
  spd:          { light: '#d0141e', dark: '#ec4a4f', usage: 'SPD' },
  ssw:          { light: '#003c8f', dark: '#4f7fcf', usage: 'SSW' },
  'party-other': { light: '#8a8d96', dark: '#6f727a', usage: 'Any party without its own colour' },
};

export const FONTS = {
  serif: '"Literata", Georgia, "Times New Roman", serif',
  sans: '"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif',
  mono: '"IBM Plex Mono", ui-monospace, "Cascadia Mono", Consolas, monospace',
};

export const LAYOUT = {
  /** Width of the reading column. */
  'page-width': '860px',
  /** Width of the home page and the top bar, where cards sit four abreast. */
  'wide-width': '1100px',
  /** Side gutter at phone width. */
  gutter: '16px',
  radius: '6px',
  /** Home cards and link cards. */
  'radius-lg': '12px',
};

/** The CSS variable a party is drawn with. */
export function partyVar(id: string): string {
  return id in PARTY_COLORS ? `var(--party-${id})` : 'var(--party-party-other)';
}

function block(mode: 'light' | 'dark'): string {
  const colors = Object.entries(COLORS).map(([k, t]) => `--${k}:${t[mode]};`);
  const parties = Object.entries(PARTY_COLORS).map(([k, t]) => `--party-${k}:${t[mode]};`);
  return [...colors, ...parties].join('');
}

/** Write every token as a CSS custom property, before anything renders. */
export function installTokens(): void {
  const fixed = [
    ...Object.entries(FONTS).map(([k, v]) => `--${k}:${v};`),
    ...Object.entries(LAYOUT).map(([k, v]) => `--${k}:${v};`),
  ].join('');
  const css =
    `:root{color-scheme:light;${fixed}${block('light')}}` +
    `@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;${block('dark')}}}` +
    `:root[data-theme="dark"]{color-scheme:dark;${block('dark')}}`;
  const style = document.createElement('style');
  style.id = 'tokens';
  style.textContent = css;
  document.head.appendChild(style);
}
