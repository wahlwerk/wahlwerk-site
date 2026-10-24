<script lang="ts">
  // Formulas page: every formula of wahlwerk.calc, by layer, as its docstrings write
  // it (build.py reads them into formulas.json; nothing here is typed by hand), with
  // the one table of symbols they all use and the literature they cite.
  import type { Formulas, References } from '../lib/types';
  import { citer } from '../lib/citations';
  import { apiHref } from '../lib/api';
  import CodeRef from './CodeRef.svelte';
  import Math from './Math.svelte';
  import Segments from './Segments.svelte';
  import RefList from './RefList.svelte';

  export let formulas: Formulas | null;
  export let references: References | null;

  $: modules = formulas ? formulas.layers.flatMap((l) => l.modules) : [];
  $: literature = [...new Set(modules.flatMap((m) => m.cites))];
  $: cite = citer(literature);
  $: groups = formulas
    ? [...new Set(formulas.symbols.map((s) => s.group))].map((g) => ({
        group: g,
        symbols: formulas!.symbols.filter((s) => s.group === g),
      }))
    : [];
</script>

<section>
  <h2>Written once</h2>
  <div class="prose">
    <p>
      Every number the engine derives comes from a <b>formula</b>: a divisor method dividing seats,
      a quota, a threshold, a majority, a measure of how proportional a result is. Each formula is
      a plain function in one part of the engine, <code>wahlwerk.calc</code>, which knows nothing
      of laws, parties or the rest of the engine: numbers in, numbers out. The engine computes only through it, so a
      step in a law and a formula called by hand give the same seats.
    </p>
    <p>
      A formula takes a table of options and numbers (votes per party, seats per caucus) and returns
      one in the same shape, or one number. Whole numbers and fractions are computed exactly, as an
      electoral law requires; decimals in floating point, fast, for polls and sweeps over many
      scenarios at once. Where the law leaves a seat to the lot, a seat formula does not draw: it
      returns the options that are tied.
    </p>
  </div>
  <CodeRef names={['wahlwerk.calc.divisor.sainte_lague', 'wahlwerk.calc.result.SeatResult', 'wahlwerk.state.chamber.Chamber']} />
</section>

{#if !formulas}
  <section><p class="muted">Loading the formulas …</p></section>
{:else}
  <section>
    <h2>Notation</h2>
    <p class="prose">One symbol, one meaning, in every formula below and in the API reference.</p>
    <div class="table-wrap">
      <table class="symbols">
        <tbody>
          {#each groups as g}
            <tr class="group"><th colspan="2">{g.group}</th></tr>
            {#each g.symbols as s}
              <tr><td class="sym"><Math tex={s.latex} /></td><td>{s.meaning}</td></tr>
            {/each}
          {/each}
        </tbody>
      </table>
    </div>
  </section>

  {#each formulas.layers as layer, i}
    <section>
      <h2><span class="layer">Layer {i + 1}</span> {layer.title}</h2>
      {#each layer.modules as m}
        <h3 id={m.qualname}><a href={apiHref(m.qualname)}><code>{m.name}</code></a></h3>
        <p class="prose lead"><Segments segments={m.title} {cite} /></p>
        {#each m.body as b}
          {#if 'p' in b}
            <p class="prose"><Segments segments={b.p} {cite} /></p>
          {:else if 'list' in b}
            <ul class="prose">
              {#each b.list as item}<li><Segments segments={item} {cite} /></li>{/each}
            </ul>
          {:else if 'math' in b}
            <Math tex={b.math} display />
          {:else if 'table' in b}
            <div class="table-wrap">
              <table>
                <thead>
                  <tr>{#each b.table.head as h}<th><Segments segments={h} {cite} /></th>{/each}</tr>
                </thead>
                <tbody>
                  {#each b.table.rows as row}
                    <tr>{#each row as c}<td><Segments segments={c} {cite} /></td>{/each}</tr>
                  {/each}
                </tbody>
              </table>
            </div>
          {/if}
        {/each}
        {#if m.functions.length}
          <dl class="functions">
            {#each m.functions as f}
              <dt><a href={apiHref(f.qualname)}><code>{f.name}{f.kind === 'function' ? '()' : ''}</code></a></dt>
              <dd><Segments segments={f.summary} {cite} /></dd>
            {/each}
          </dl>
        {/if}
      {/each}
    </section>
  {/each}

  <RefList {references} {literature} />
  <p class="muted small">Formulas of wahlwerk {formulas.calc}.</p>
{/if}

<style>
  .layer {
    font: 600 0.72rem/1 var(--sans);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent);
    margin-right: 6px;
  }
  h3 a {
    text-decoration: none;
  }
  .lead {
    color: var(--muted);
  }
  .symbols .group th {
    font: 600 0.72rem/1 var(--sans);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    text-align: left;
    padding-top: 14px;
  }
  .symbols .sym {
    white-space: nowrap;
    width: 1%;
    padding-right: 20px;
  }
  .functions {
    display: grid;
    grid-template-columns: max-content minmax(0, 1fr);
    gap: 6px 16px;
    margin: 10px 0 22px;
    font-size: 0.92rem;
  }
  .functions dt a {
    text-decoration: none;
  }
  .functions dd {
    margin: 0;
  }
  @media (max-width: 600px) {
    .functions {
      grid-template-columns: 1fr;
      gap: 2px;
    }
    .functions dd {
      margin-bottom: 8px;
    }
  }
  .small {
    font-size: 0.8rem;
  }
</style>
