/**
 * What the page says about each election, beside the numbers build.py derives.
 * Prose only: every count shown on the page comes from elections.json.
 */

export interface ElectionText {
  /** Tab label. */
  label: string;
  /** What is special about this election under its law. */
  note: string;
}

export const ELECTION_TEXT: Record<string, ElectionText> = {
  'de.landtag.st.2026': {
    label: 'Sachsen-Anhalt 2026',
    note:
      'No Mehrsitze, and § 35 (6) does not apply: the AfD has 47 % of the Zweitstimmen that count, not more than half.',
  },
  'de.landtag.st.2021': {
    label: 'Sachsen-Anhalt 2021',
    note:
      'The CDU won 40 of 41 Wahlkreise, so § 35 (8) raised the house from 83 to 97 in two rounds and balanced every Mehrsitz. All 40 CDU seats are Wahlkreis seats.',
  },
  'de.landtag.mv.2021': {
    label: 'Mecklenburg-Vorpommern 2021',
    note:
      'The SPD won 34 of 36 Wahlkreise, 3 more than its 31 seats of 71. § 58 (6) LKWG M-V raised the house to 78 to balance the Überhang, and to 79 to make it odd.',
  },
  'de.landtag.mv.2016': {
    label: 'Mecklenburg-Vorpommern 2016',
    note: 'No Überhang: no party won more Wahlkreise than its share of 71 seats.',
  },
  'de.landtag.mv.2011': {
    label: 'Mecklenburg-Vorpommern 2011',
    note: 'No Überhang: no party won more Wahlkreise than its share of 71 seats.',
  },
};
