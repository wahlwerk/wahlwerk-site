<script lang="ts">
  // Vote › Tally: the record a popular vote leaves. One long table of counts, the
  // options beside it, the kinds of count, and the operations that sum it up to what a
  // law decides on (decision 0009 in the engine's notes).
  import type { References, Sketches } from '../lib/types';
  import { href } from '../lib/pages';
  import CodeRef from './CodeRef.svelte';
  import Plate from './Plate.svelte';
  import RefList from './RefList.svelte';
  import Term from './Term.svelte';

  export let sketches: Sketches | null;
  export let references: References | null;

  const DATA = ['de.landtag.st.2026'] as const;
  const T = 'wahlwerk.vote.popular.tally';

  const tallyCsv = `# tally.csv
unit,level,kind,section,channel,option,count
de.st.gem.15081026.wbz.000001,wahlbezirk,eligible,,,,590
de.st.gem.15081026.wbz.000001,wahlbezirk,voters,,urne,,433
de.st.gem.15081026.wbz.000001,wahlbezirk,invalid,zweitstimme,urne,,4
de.st.gem.15081026.wbz.000001,wahlbezirk,votes,zweitstimme,urne,cdu,61
de.st.gem.15081026.wbz.000001,wahlbezirk,votes,erststimme,urne,cdu,80
...`;

  const optionsCsv = `# options.csv
option,party
cdu,cdu
afd,afd
...
de.st.wk.005.einzelbewerber,`;

  const operations = [
    { name: 'Select', code: 'tally.filter(kind="votes", section="zweitstimme")', does: 'keeps the rows that match: one section, one kind, one channel' },
    { name: 'RollUp', code: 'tally.sum_to("wahlkreis", hierarchy=electoral)', does: 'sums the units into the larger units of a tree' },
    { name: 'Relabel', code: 'tally.relabel("section", {...})', does: 'renames or merges what is counted: two sections as one, a candidate as their party' },
    { name: 'Collapse', code: 'tally.collapse("channel")', does: 'sums a field away: polling station and post together' },
  ];
</script>

<section>
  <h2>One long table</h2>
  <p>
    A <b>tally</b> is a list of counts, one <b>row</b> per count. A row says where it was
    counted (its unit and the unit's level), what it counts (its kind, its section, its channel
    and the option the votes are for) and how many. Nothing else is on a row: no total, no
    share, no party. Every count a vote leaves is a row of this one table, the people registered
    and voting as much as the votes, so the archive and the engine hold the same thing: the file
    <code>tally.csv</code> is the table.
  </p>
  <pre><code>{tallyCsv}</code></pre>
  <p>
    The rows are the first of one <Term t="Wahlbezirk" /> in the
    <a href="#data-de.landtag.st.2026">Landtagswahl Sachsen-Anhalt 2026</a>.
    A blank cell is absent, never zero. Totals are never stored: the valid votes of a
    <Term t="Wahlkreis" />, the <Term t="Gültige" /> of the <Term t="Land" />, are sums of rows,
    and whatever needs them sums. A row the counting could not have produced is refused when the
    tally is read, with the line it stands on.
  </p>
  {#if sketches}<Plate plate={sketches.plates.recorded} />{/if}
  <CodeRef names={[`${T}.Tally`, `${T}.TallyRow`, 'wahlwerk.io.bundle.read_bundle']} />
</section>

<section>
  <h2>Kinds of count</h2>
  <p>
    Four kinds cover what most tallies count: <code>eligible</code> and <code>voters</code>
    count people, in no section; <code>invalid</code> and <code>votes</code> count votes, each
    in its section, and only <code>votes</code> name an option. A kind decides which fields its
    rows set, nothing more. Which kinds are <b>valid</b>, and what a law counts them towards, is
    the law's, not the tally's.
  </p>
  <p>
    The list is open. A vote that records more, blank papers counted apart from invalid ones, or
    voters by how they voted, declares each further kind beside the tally, saying whether it
    counts people or votes and whether its rows name an option; a row of a kind nobody declared is
    refused.
  </p>
  <CodeRef names={[`${T}.TallyKind`, `${T}.Kind`]} />
</section>

<section>
  <h2>Options beside the rows</h2>
  <p>
    A row names the <b>option</b> its votes count for: a party's list, a candidate, an answer such
    as yes. Which party an option stands for is not on the row. It is a fact about the option,
    the same in every unit, so it is written once beside the table: a list stands for its party,
    a candidate for the party that nominated them, an <Term t="Einzelbewerber" /> or an answer for
    none.
  </p>
  <pre><code>{optionsCsv}</code></pre>
  <p>
    In the example the <Term t="Erststimme">Erststimmen</Term> count for a party's nominee, whose
    name the source does not give, so the option is the party itself; an
    <Term t="Einzelbewerber" /> is an option of their own, for no party. A source that names its
    candidates gives each an option of their own, standing for their party.
  </p>
  <p>
    Counting by party is then a relabel along this map: a nominee's
    <Term t="Erststimme">Erststimmen</Term> go to their party, an independent's to no party and
    so out of a table by party. Further maps of the same kind, lists joined into one, a candidate
    put up by two parties, would sit here too, once a law needs them.
  </p>
  <CodeRef names={[`${T}.Option`, `${T}.Tally.party_of`]} />
</section>

<section>
  <h2>The way up</h2>
  <p>
    A law never decides on the rows. It decides on sums: the votes of each option in each
    <Term t="Wahlkreis" />, the votes of each party in the <Term t="Land" />. Getting there is a
    short sequence of four operations, each returning a tally again. Laws differ in the sequence,
    not in the operations; whatever is not a sum (a threshold, a seat method) is a step of the
    law.
  </p>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Operation</th><th>In the code</th><th>Does</th></tr></thead>
      <tbody>
        {#each operations as op}
          <tr><td>{op.name}</td><td><code>{op.code}</code></td><td>{op.does}</td></tr>
        {/each}
      </tbody>
    </table>
  </div>
  <p>
    The step a law counts with is these four in a row: it rolls the rows up to the level the law
    names, selects the valid votes of its section, sums the channels away and lays the result out
    by option or by party. Counting two sections as one, as a law that adds
    <Term t="Erststimme">Erst-</Term> and <Term t="Zweitstimme">Zweitstimmen</Term> does, is one
    more relabel in the same row. Which tree the units are rolled up along is on the
    <a href={href('vote-hierarchies')}>Hierarchies</a> page.
  </p>
  <CodeRef
    names={[
      `${T}.Tally.filter`,
      `${T}.Tally.sum_to`,
      `${T}.Tally.relabel`,
      `${T}.Tally.collapse`,
      'wahlwerk.process.allocation.count.SumGroupBy',
    ]}
  />
</section>

<section>
  <h2>What a tally cannot hold</h2>
  <p>
    Each row counts one section. What one voter did across sections, or the order of their
    preferences, is lost in the sums: the <Term t="Zweitstimme">Zweitstimmen</Term> of the voters
    who elected an <Term t="Einzelbewerber" /> cannot be read off the rows. Such counts, where a
    source publishes them, will be a section of their own whose options are combinations, each
    naming its part in every section; a law that moves particular papers needs the papers
    themselves. Neither is held yet.
  </p>
</section>

<RefList {references} data={DATA} />
