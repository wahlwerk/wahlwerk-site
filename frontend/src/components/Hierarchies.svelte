<script lang="ts">
  // How a unit id carries the electoral hierarchy, and the administrative
  // one that sits beside it as an explicit tree.
  const segments = [
    { text: 'de.st', label: 'Land · 2', color: 'var(--accent)' },
    { text: 'wk.035', label: 'Wahlkreis · 4', color: 'var(--party-afd)' },
    { text: 'gem.15002000.wbz.000001', label: 'Wahlbezirk · 8', color: 'var(--party-linke)' },
  ];

  const electionToml = `# election.toml
schema = 2

[levels]
land = 2
wahlkreis = 4
wahlbezirk = 8
briefwahlbezirk = 8

[hierarchies.administrative]
levels = ["land", "kreis", "gemeinde"]`;

  const administrativeCsv = `# administrative.csv
unit,level,parent
de.st,land,
de.st.krs.15002,kreis,de.st
de.st.gem.15002000,gemeinde,de.st.krs.15002
de.st.wk.035.gem.15002000.wbz.000001,
  wahlbezirk,de.st.gem.15002000`;
</script>

<section>
  <h2>Two hierarchies</h2>
  <p>
    The units of a tally belong to two hierarchies that cross. The <b>electoral</b> one (Land,
    Wahlkreis, Wahlbezirk) is what the law counts along, so it is the main one and the unit ids
    follow it. The <b>administrative</b> one (Land, Kreis, Gemeinde, Wahlbezirk) is for analysis.
    Halle, Magdeburg and Dessau-Roßlau each lie in several Wahlkreise, so it cannot be read off
    the ids, and it sits beside the main one as its own tree.
  </p>

  <h3>Main: in the ids</h3>
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
    The unit a row lies in is a prefix of its id, so summing up means cutting the id. The
    Gemeindeschlüssel is part of the Wahlbezirk's id because Wahlbezirk numbers are only unique
    within a Gemeinde. <code>tally.sum_to("wahlkreis")</code> takes the depth from
    <code>[levels]</code>.
  </p>

  <h3>Beside it: an explicit tree</h3>
  <div class="two">
    <pre><code>{electionToml}</code></pre>
    <pre><code>{administrativeCsv}</code></pre>
  </div>
  <p>
    <code>tally.sum_to("gemeinde", hierarchy=admin)</code> sums Halle's Wahlbezirke in four
    Wahlkreise into one Gemeinde. The hierarchy is checked to be a tree and to cover every counted
    unit. The law is never evaluated along an alternative hierarchy.
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
