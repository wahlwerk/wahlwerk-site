<script lang="ts">
  // A unit id names its unit only; every grouping of units, the electoral one
  // included, is an explicit tree beside the rows (bundle schema 4, decision 0009).
  import Term from './Term.svelte';
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
  <h2>Two hierarchies</h2>
  <p>
    The units of a tally belong to two hierarchies that cross. The <b>electoral</b> one (Land,
    Wahlkreis, Wahlbezirk) is what the law counts along. The <b>administrative</b> one (Land,
    Kreis, Gemeinde, Wahlbezirk) is for analysis: Halle, Magdeburg and Dessau-Roßlau each lie in
    several Wahlkreise, so neither tree can be read off the other.
  </p>

  <h3>An id names its unit</h3>
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

  <h3>Every grouping a tree</h3>
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
</section>

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
