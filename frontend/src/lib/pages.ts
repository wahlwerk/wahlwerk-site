/**
 * The pages of the site and the hash routes that reach them. The four
 * component pages follow the engine's roles in order, so the home cards, the
 * top navigation and the prev/next links all read from this one list.
 */

export type ComponentId = 'vote' | 'law' | 'allocation' | 'chamber';
export type PageId = 'home' | ComponentId | 'impressum' | 'style';

export interface ComponentPage {
  id: ComponentId;
  /** The engine's role for this component. */
  role: 'input' | 'protocol' | 'process' | 'state';
  title: string;
  /** One sentence under the page title. */
  lede: string;
  /** What the home card says. */
  card: string;
}

export const COMPONENTS: ComponentPage[] = [
  {
    id: 'vote',
    role: 'input',
    title: 'Vote',
    lede:
      'What the electorate recorded: a tally of rows, one per unit, section and party, with its source. The vote holds no law.',
    card:
      'The tally as the engine reads it: units from Land to Wahlbezirk, and the two hierarchies they belong to.',
  },
  {
    id: 'law',
    role: 'protocol',
    title: 'Law',
    lede:
      'An electoral law written as an ordered tuple of steps, each citing the paragraph it follows.',
    card:
      'The Landeswahlgesetz of Sachsen-Anhalt as a protocol: every step, its paragraph, and the loop of § 35 (8).',
  },
  {
    id: 'allocation',
    role: 'process',
    title: 'Allocation',
    lede:
      'allocate(vote, protocol) applies each step to one working record and forms a chamber. It belongs to neither the vote nor the chamber.',
    card:
      'How the pieces fit: apportionment methods, thresholds, Ausgleich, and the process that runs the law.',
  },
  {
    id: 'chamber',
    role: 'state',
    title: 'Chamber',
    lede:
      'The chamber the engine derives from the votes, equal to the official Sitzverteilung party by party.',
    card:
      'Every golden election seat by seat: Wahlkreis and list seats, votes and shares, and the source of each.',
  },
];

const ALL: PageId[] = ['home', ...COMPONENTS.map((c) => c.id), 'impressum', 'style'];

/** The page a location hash names; anything unknown is home. */
export function pageFromHash(hash: string): PageId {
  const id = hash.replace(/^#\/?/, '');
  return (ALL as string[]).includes(id) ? (id as PageId) : 'home';
}

export function href(page: PageId): string {
  return page === 'home' ? '#/' : `#/${page}`;
}
