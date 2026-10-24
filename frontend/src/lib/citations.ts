/**
 * References, three kinds from three homes (build.py, references.py):
 *
 * - Literature, from the engine's docs/references.bib (Zotero): cited in running
 *   text as a superscript number, listed in full at the foot of the page in the
 *   IR-bands form (authors with initials, title, container, year, DOI or URL link).
 * - Statutes, from the engine's law registry, one entry per version: cited inline in
 *   the German form with the section (Sec. 35 (8) LWG LSA, Art. 63 GG), linked to the
 *   list, which gives the version's Fassung, the dates it was in force and its source.
 *   Laws are never in Zotero: they change by amendment and are cited by version.
 * - Data, from each bundle's [source]: named under the result or sketch it fed,
 *   with publisher, licence and the attribution the publisher requires.
 */
import type { DataSource, Reference, Statute } from './types';

export function strip(s: string | undefined): string {
  return (s ?? '').replace(/[{}]/g, '');
}

function esc(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/** "Wachs, Israel E. and Bañares, Miguel A." as "I. E. Wachs and M. A. Bañares". */
export function authors(raw: string): string {
  const names = strip(raw)
    .split(/\s+and\s+/i)
    .map((a) => a.trim())
    .filter(Boolean)
    .map((a) => {
      if (!a.includes(',')) return a; // an institution, or a name already in order
      const [last, first] = a.split(',', 2).map((s) => s.trim());
      const initials = first
        .split(/\s+/)
        .filter(Boolean)
        .map((n) => n[0] + '.')
        .join(' ');
      return initials ? `${initials} ${last}` : last;
    });
  if (names.length <= 1) return names[0] ?? '';
  if (names.length === 2) return `${names[0]} and ${names[1]}`;
  return names.slice(0, -1).join(', ') + ', and ' + names[names.length - 1];
}

/** Where a reference lives on the web: its DOI, else its URL, else nothing. */
export function refHref(ref: Reference): string {
  const doi = strip(ref.doi);
  if (doi) return doi.startsWith('http') ? doi : `https://doi.org/${doi}`;
  return strip(ref.url);
}

/** One work of literature in full, as HTML: articles quoted, books set italic. */
export function referenceHtml(ref: Reference | undefined, key: string): string {
  if (!ref) return `<span class="missing">${esc(key)}: not in references.bib</span>`;
  const isWork = ['article', 'inproceedings', 'incollection', 'inbook'].includes(ref.type);
  const title = strip(ref.title);
  const short = strip(ref.shorttitle);
  const container = strip(ref.journaltitle ?? ref.journal ?? ref.booktitle);
  const year = strip(ref.date ?? ref.year);
  const parts: string[] = [];
  if (ref.author) parts.push(esc(authors(ref.author)));
  if (title) {
    const t = isWork ? `&ldquo;${esc(title)}&rdquo;` : `<em>${esc(title)}</em>`;
    parts.push(short && !isWork ? `${t} (${esc(short)})` : t);
  }
  if (container) parts.push(`<em>${esc(container)}</em>`);
  const detail = [
    ref.volume && `vol.&nbsp;${esc(strip(ref.volume))}`,
    ref.number && `no.&nbsp;${esc(strip(ref.number))}`,
    ref.pages && `pp.&nbsp;${esc(strip(ref.pages).replace(/--/g, '–'))}`,
  ].filter(Boolean);
  if (detail.length) parts.push(detail.join(', '));
  if (ref.publisher) parts.push(esc(strip(ref.publisher)));
  if (year) parts.push(esc(ref.type === 'legislation' ? year : year.slice(0, 4)));
  let html = parts.join(', ') + '.';
  if (ref.note) html += ` ${esc(strip(ref.note))}.`;
  const href = refHref(ref);
  if (href) html += ` <a href="${href}" target="_blank" rel="noopener noreferrer">↗</a>`;
  return html;
}

/** A page's citer: keys numbered by first citation, in the order the page lists them. */
export function citer(order: readonly string[]): (key: string) => number {
  return (key: string) => {
    const i = order.indexOf(key);
    if (i < 0) throw new Error(`cited ${key}, which the page does not list`);
    return i + 1;
  };
}

/** One statute version in full, as HTML: its title, the Fassung, when it was in force. */
export function statuteHtml(s: Statute | undefined, id: string): string {
  if (!s) return `<span class="missing">${esc(id)}: not in the law registry</span>`;
  let html = `<em>${esc(s.title)}</em> (${esc(s.short)}), ${esc(s.citation)}.`;
  const from = s.in_force_from;
  const until = s.in_force_until;
  if (from || until) html += ` In force ${from ? `from ${esc(from)}` : ''}${from && until ? ' ' : ''}${until ? `until ${esc(until)}` : ''}.`;
  html += s.implemented ? ` Engine: <code>${esc(id)}</code>.` : '';
  if (s.source) html += ` <a href="${s.source}" target="_blank" rel="noopener noreferrer">↗</a>`;
  return html;
}

/** One data source in full, as HTML, with the attribution its licence requires. */
export function dataHtml(d: DataSource | undefined, key: string): string {
  if (!d) return `<span class="missing">${esc(key)}: no bundle</span>`;
  let html = `${esc(d.publisher)}, <em>${esc(d.title)}</em>.`;
  if (d.licence) html += ` Licence ${esc(d.licence)}.`;
  if (d.attribution) html += ` ${esc(d.attribution)}`;
  if (d.url) html += ` <a href="${d.url}" target="_blank" rel="noopener noreferrer">↗</a>`;
  return html;
}
