<script lang="ts">
  // A unit id names its unit only; every grouping of units, the electoral one
  // included, is an explicit tree beside the rows (bundle schema 4, decision 0009).
  import type { References } from '../lib/types';
  import CodeRef from './CodeRef.svelte';
  import RefList from './RefList.svelte';
  import Term from './Term.svelte';

  export let references: References | null;

  const DATA = ['de.landtag.st.2026'] as const;
  const H = 'wahlwerk.vote.popular.hierarchy';
  const segments = [
    { text: 'de.st', label: 'Land', color: 'var(--accent)' },
    { text: 'gem.15002000', label: 'Gemeinde', color: 'var(--party-afd)' },
    { text: 'wbz.000001', label: 'Wahlbezirk', color: 'var(--party-linke)' },
  ];

  const electionToml = `# election.toml
schema = 4

[hierarchies.electoral]
levels = ["land", "wahlkreis"]

[hierarchies.administrative]
levels = ["land", "kreis", "gemeinde"]`;

  const trees = `# electoral.csv
unit,level,parent
de.st,land,
de.st.wk.035,wahlkreis,de.st
de.st.gem.15002000.wbz.000001,
  wahlbezirk,de.st.wk.035

# administrative.csv
unit,level,parent
de.st,land,
de.st.krs.15002,kreis,de.st
de.st.gem.15002000,gemeinde,de.st.krs.15002
de.st.gem.15002000.wbz.000001,
  wahlbezirk,de.st.gem.15002000`;
</script>

<section>
  <h2>Trees that cross</h2>
  <p>
    The units of a tally belong to two hierarchies that cross. The <b>electoral</b> one (Land,
    Wahlkreis, Wahlbezirk) is what the law counts along. The <b>administrative</b> one (Land,
    Kreis, Gemeinde, Wahlbezirk) is for analysis: Halle, Magdeburg and Dessau-Roßlau each lie in
    several Wahlkreise, so neither tree can be read off the other.
  </p>

  <CodeRef names={[`${H}.Hierarchy`, `${H}.HierarchyUnit`]} />
</section>

<section>
  <h2>An id names its unit</h2>
  <div class="uid" aria-label={segments.map((s) => s.text).join('.')}>
    {#each segments as seg, i}
      {#if i > 0}<span class="dot">.</span>{/if}
      <div class="seg" style="--c:{seg.color}">
        <code class="t">{seg.text}</code>
        <small>{seg.label}</small>
      </div>
    {/each}
  </div>
  <p>
    The id says which unit a row was counted in and nothing about what it lies in. The
    Gemeindeschlüssel is part of it because Wahlbezirk numbers are only unique within a
    Gemeinde. The <Term t="Wahlkreis" /> is not: the Wahlkreise are drawn by the law, in an annex
    that changes between versions, so the same votes can be counted along the Wahlkreise of
    another version without touching the rows.
  </p>

</section>

<section>
  <h2>Every grouping a tree</h2>
  <div class="two">
    <pre><code>{electionToml}</code></pre>
    <pre><code>{trees}</code></pre>
  </div>
  <p>
    A law names the tree it counts along, by default <code>electoral</code>:
    <code>tally.sum_to("wahlkreis", hierarchy=electoral)</code> gives its Wahlkreise, and
    <code>tally.sum_to("gemeinde", hierarchy=admin)</code> sums Halle's Wahlbezirke in four
    Wahlkreise into one Gemeinde. Each tree is checked to be a tree and to cover every counted
    unit. Which party an option stands for sits beside the rows in the same way, once per
    option, in <code>options.csv</code>.
  </p>
  <p>
    Any further tree is one more file. The archive's bundle of the Berlin
    <Term t="Abgeordnetenhaus" /> election of 2026 carries two besides its electoral one, the halves of the city and the <Term t="Bundestag" /> constituencies, so
    the same rows can be summed along either; the Wahlkreise of another version of a law would be
    one more tree over the same rows, and a law that names it counts along it.
  </p>
  <CodeRef
    names={[
      `${H}.Hierarchy.units_at`,
      'wahlwerk.vote.popular.tally.Tally.sum_to',
      'wahlwerk.process.allocation.count.SumGroupBy',
    ]}
  />
</section>

<section>
  <h2>What a tree cannot do</h2>
  <p>
    Every unit has one parent, so a unit lies wholly in one larger unit. A unit cut in two by a
    new boundary, a <Term t="Wahlbezirk" /> split between two Wahlkreise, would need part of
    its count on each side: a weighted map, whose sums are estimates, fit for an analysis and
    never for a result. Neither that nor a unit counted in two districts at once is held yet. One
    unit in the archive keeps its <Term t="Wahlkreis" /> in its id: where the source numbers a
    unit only within its Wahlkreis, two units would otherwise share one id.
  </p>
</section>

<RefList {references} data={DATA} />

<style>
  .uid {
    font: 500 clamp(0.8rem, 2.6vw, 1.05rem)/1 var(--mono);
    display: flex;
    flex-wrap: wrap;
    gap: 4px 0;
  }
  .seg {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }
  .seg code {
    background: none;
    padding: 0 1px;
    font-size: inherit;
    overflow-wrap: anywhere;
  }
  .seg .t {
    padding: 6px 8px;
    border-top: 3px solid var(--c);
    background: var(--surface);
  }
  .seg small {
    font: 500 0.7rem var(--sans);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--muted);
  }
  .dot {
    align-self: flex-start;
    padding-top: 9px;
    color: var(--muted);
  }
</style>
