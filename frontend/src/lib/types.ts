/** The shape of docs/data/elections.json, as build.py writes it. */

export interface PartyResult {
  id: string;
  name: string;
  short_name: string;
  /** Zweitstimmen in the Land. */
  votes: number;
  seats: number;
  /** Seats won in a Wahlkreis. */
  wahlkreis: number;
  /** Seats from the Landesliste. */
  list: number;
}

export interface Election {
  /** Bundle key in wahlwerk-data, e.g. de.landtag.st.2026. */
  key: string;
  body: string;
  /** Election day, ISO date. */
  date: string;
  law: { id: string; title: string; citation: string };
  source: {
    publisher: string;
    title: string;
    url: string | null;
    licence: string | null;
    attribution: string | null;
  };
  /** Size of the chamber the engine formed. */
  seats: number;
  /** Valid Zweitstimmen of every party, seated or not. */
  valid_votes: number;
  /** Seated parties, most seats first. */
  parties: PartyResult[];
}

export interface SiteData {
  /** The wahlwerk version that derived the numbers. */
  engine: string;
  elections: Election[];
}
