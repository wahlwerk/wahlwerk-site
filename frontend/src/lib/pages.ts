/**
 * The pages of the site and the hash routes that reach them. The component
 * pages follow the engine's roles in order, the formulas they compute with last, so the home cards, the
 * top navigation and the prev/next links all read from this one list.
 */

export type ComponentId = 'vote' | 'law' | 'chamber' | 'formulas';
export type PageId =
  | 'home'
  | ComponentId
  | 'vote-tally'
  | 'vote-hierarchies'
  | 'vote-lot'
  | 'law-allocation'
  | 'law-steps'
  | 'impressum'
  | 'style';

/** Pages under a component page: shown under it in the side panel, reached by a path. */
export const SUBPAGES: { id: PageId; parent: ComponentId; title: string; path: string; lede: string }[] = [
  {
    id: 'vote-tally',
    parent: 'vote',
    title: 'Tally',
    path: 'vote/tally',
    lede: 'The record a popular vote leaves: one long table of counts, the options beside it, and the few operations that sum it up to what a law decides on.',
  },
  {
    id: 'vote-hierarchies',
    parent: 'vote',
    title: 'Hierarchies',
    path: 'vote/hierarchies',
    lede: 'How the units of a tally group into larger ones: every grouping is a tree beside the rows, and a law names the one it counts along.',
  },
  {
    id: 'vote-lot',
    parent: 'vote',
    title: 'Lot',
    path: 'vote/lot',
    lede: 'Where equal claims are decided by lot, the engine never draws: a tie is a result, and the lot actually drawn is recorded with the vote.',
  },
  {
    id: 'law-allocation',
    parent: 'law',
    title: 'Allocation',
    path: 'law/allocation',
    lede:
      'allocate(vote, protocol) runs a law: it applies each step to one working record and forms a chamber. It belongs to neither the vote nor the chamber.',
  },
  {
    id: 'law-steps',
    parent: 'law',
    title: 'Steps',
    path: 'law/steps',
    lede: 'Every kind of step the laws on this site are made of: what it does, what it reads and writes, what it computes with, and where each law uses it.',
  },
];

/** Old routes kept working: the Allocation page moved under Law. */
const MOVED: Record<string, PageId> = { allocation: 'law-allocation' };

export interface ComponentPage {
  id: ComponentId;
  /** The engine's role for this component. */
  role: 'input' | 'protocol' | 'state' | 'formula';
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
      'How many choices become one record: who votes, on what, and what is recorded. The vote is input and holds no law.',
    card:
      'What a vote is: the electorate and the members of a body, what they vote on, and the tally a popular vote leaves.',
  },
  {
    id: 'law',
    role: 'protocol',
    title: 'Law',
    lede:
      'A law is a list of steps, each citing the paragraph it follows. What depends on what follows from the facts each step reads and writes.',
    card:
      'Two Landtag laws as protocols, and the allocation that runs them: every step and its paragraph, drawn down to its formula; which steps depend on which, and which could trade places.',
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
  {
    id: 'formulas',
    role: 'formula',
    title: 'Formulas',
    lede:
      'Every formula the engine computes with, each written once in wahlwerk.calc: seat methods, quotas, thresholds, majorities, measures, coalitions and power.',
    card:
      'The arithmetic under every step, in one notation: divisor and quota methods, proportionality, the effective number of parties, Banzhaf and Shapley-Shubik.',
  },
];

const ALL: PageId[] = ['home', ...COMPONENTS.map((c) => c.id), 'impressum', 'style'];

/** The page a location hash names; anything unknown is home. */
export function pageFromHash(hash: string): PageId {
  const id = hash.replace(/^#\/?/, '');
  const sub = SUBPAGES.find((s) => s.path === id);
  if (sub) return sub.id;
  if (MOVED[id]) return MOVED[id];
  return (ALL as string[]).includes(id) ? (id as PageId) : 'home';
}

export function href(page: PageId): string {
  const sub = SUBPAGES.find((s) => s.id === page);
  if (sub) return `#/${sub.path}`;
  return page === 'home' ? '#/' : `#/${page}`;
}
