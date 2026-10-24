/**
 * Terms of art: the names one system gives to a general concept.
 *
 * The site writes about concepts in plain words (a chamber, a unit, a section) and
 * sets a term of art, the kind one system has of that concept, in italics with a
 * dotted underline (components/Term.svelte). Hovering it says which concept it is an
 * instance of and in which system. The four roles of text on the site:
 *
 *   concept       plain; bold where it is defined          a chamber, the tally
 *   term of art   italic, dotted underline, from here      Landtag, Wahlkreis
 *   code          monospace, linked to the API reference   TallyRow, vote/chamber/
 *   statute       the law style, linked to its version     Art. 63 GG
 *
 * One entry per term, in the form the system itself uses; a plural or another case is
 * written in the page and the entry named with `t` (<Term t="Wahlkreis">Wahlkreise</Term>).
 */

export interface GlossaryEntry {
  /** The general concept this term is an instance of, as the engine names it. */
  concept: string;
  /** The system it belongs to, jurisdiction first (de, de.bund, ie). */
  system: string;
  /** What it is, in one line. */
  gloss: string;
}

export const GLOSSARY: Record<string, GlossaryEntry> = {
  // bodies and offices
  Bundestag: { concept: 'chamber', system: 'de.bund', gloss: 'the federal parliament of Germany' },
  Landtag: { concept: 'chamber', system: 'de', gloss: 'the parliament of a German Land' },
  Gemeinderat: { concept: 'chamber', system: 'de', gloss: 'the council of a German municipality' },
  Bundesrat: {
    concept: 'body',
    system: 'de.bund',
    gloss: 'the body through which the German Länder take part in federal legislation',
  },
  Bundesversammlung: { concept: 'body', system: 'de.bund', gloss: 'the body that elects the German Federal President' },
  Dáil: { concept: 'chamber', system: 'ie', gloss: 'the lower house of the Irish parliament' },
  Bundeskanzler: { concept: 'office', system: 'de.bund', gloss: 'the head of the German federal government, elected by the Bundestag' },
  // units
  Land: { concept: 'unit', system: 'de', gloss: 'a federal state of Germany' },
  Wahlkreis: { concept: 'unit', system: 'de', gloss: 'a unit that elects one member by plurality' },
  // seats
  Überhang: { concept: 'overhang', system: 'de', gloss: 'seats a party won in Wahlkreise beyond its proportional share' },
  Ausgleich: { concept: 'compensation', system: 'de', gloss: 'adding seats to the chamber until every party\'s Wahlkreis seats are covered proportionally' },
  Grundmandatsklausel: { concept: 'threshold', system: 'de', gloss: 'a party passes with enough Wahlkreis seats, whatever its share' },
  Wahlbezirk: { concept: 'unit', system: 'de', gloss: 'the smallest unit of a German election: one polling station, counted on its own' },
  Briefwahlbezirk: { concept: 'unit', system: 'de', gloss: 'a unit in which postal votes are counted; nobody is registered in it' },
  Gemeinde: { concept: 'unit', system: 'de', gloss: 'a municipality, a unit of the administrative hierarchy' },
  // votes, sections, channels
  Landtagswahl: { concept: 'popular vote', system: 'de', gloss: 'the election of a Landtag' },
  Volksentscheid: { concept: 'popular vote', system: 'de', gloss: 'a popular vote on a question rather than on candidates' },
  'namentliche Abstimmung': { concept: 'chamber vote', system: 'de.bund', gloss: 'a recorded vote: each member’s choice is named' },
  Stimmzettel: { concept: 'ballot paper', system: 'de', gloss: 'the paper a voter marks' },
  Erststimme: { concept: 'section', system: 'de', gloss: 'the vote for a candidate in the Wahlkreis' },
  Zweitstimme: { concept: 'section', system: 'de', gloss: 'the vote for a party list' },
  Briefwahl: { concept: 'channel', system: 'de', gloss: 'voting by post' },
  // kinds of count
  Wahlberechtigte: { concept: 'eligible', system: 'de', gloss: 'the people eligible to vote' },
  Wähler: { concept: 'voters', system: 'de', gloss: 'the people who voted' },
  Gültige: { concept: 'valid votes', system: 'de', gloss: 'the valid votes; in a tally a sum, never stored' },
  // options
  Kumulieren: { concept: 'several marks', system: 'de', gloss: 'giving one candidate more than one vote' },
  Panaschieren: { concept: 'several marks', system: 'de', gloss: 'giving votes to candidates on different lists' },
};

/** The tooltip of a term: what it is, and the concept it is an instance of. */
export function termTitle(term: string): string {
  const e = GLOSSARY[term];
  if (!e) throw new Error(`term of art ${term} is not in the glossary`);
  return `${e.gloss}. A ${e.concept} (${e.system}).`;
}
