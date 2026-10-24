<script lang="ts">
  // The Steps page, under Law: every kind of step the laws on this site are made of,
  // with what its class's docstring says it does (laws.json; the text is the engine's),
  // the facts it reads and writes, and where each law uses it with the paragraph.
  import type { Laws, References } from '../lib/types';
  import { apiHref } from '../lib/api';
  import CodeRef from './CodeRef.svelte';
  import Segments from './Segments.svelte';
  import RefList from './RefList.svelte';
  import Term from './Term.svelte';

  export let laws: Laws | null;
  export let references: References | null;

  $: statutes = laws ? laws.laws.map((l) => l.id) : [];

  // A concept inside another (method.method) is drawn inside it.
  const depth = (field: string): number => field.split('.').filter((p) => !/^\d+$/.test(p)).length - 1;
  // remainder.largest_remainder: a function by name, its module of wahlwerk.calc first;
  // what it needs stands above it.
  const name = (formula: string): string => formula.replace(/^wahlwerk\.calc\./, '');

  // The step docstrings cite no literature; a citer that is never called.
  const noCite = (key: string): number => {
    throw new Error(`unexpected citation ${key}`);
  };
</script>

<section>
  <h2>Kinds of step</h2>
  <p class="prose">
    A step is one rule, and it reads like a function: it <b>takes</b> facts as its arguments
    (<code>votes=erststimme by wahlkreis × option</code>), has settings of its own, and its results
    are the facts it writes. Each kind below is a class in the engine; a law uses it with its
    own settings and cites its own paragraph. The facts a step takes must be written by an
    earlier step; the facts it writes are what later steps can take. A table of counts is named by
    what it counts and by what: <code>erststimme by wahlkreis × option</code> has a row per
    <Term t="Wahlkreis" />, a column per option, and the <Term t="Erststimme">Erststimmen</Term>
    in it, each row one contest; <code>zweitstimme by land × party</code> adds up each party's
    <Term t="Zweitstimme">Zweitstimmen</Term>, what the seats are divided by. A step that holds steps (a sequence, a loop) reads and writes what its steps do.
  </p>
</section>

{#if !laws}
  <section><p class="muted">Loading the steps …</p></section>
{:else}
  {#each laws.kinds as k (k.kind)}
    <section class="kind">
      <h3 id="step-{k.kind}"><code>{k.kind}</code></h3>
      <p class="prose"><Segments segments={k.summary} cite={noCite} /></p>
      <dl>
        {#if k.inputs.length}
          <dt>takes</dt>
          <dd>{#each k.inputs as [arg, f]}<code class="fact">{arg}={f}</code>{/each}</dd>
        {:else}
          <dt>reads</dt>
          <dd>{#each k.reads as f}<code class="fact">{f}</code>{/each}</dd>
        {/if}
        <dt>writes</dt>
        <dd>{#each k.writes as f}<code class="fact">{f}</code>{/each}</dd>
        {#if k.computes.length}
          <dt>computes with</dt>
          <dd class="chain">
            {#each k.computes as c}
              <span class="concept" style="margin-left:{depth(c.field)}em">
                <code class="name">{c.kind}</code>
                {#if c.arguments.length || c.parameters.length}<small>{[...c.arguments, ...c.parameters].map(([p, v]) => `${p}=${v}`).join(', ')}</small>{/if}
                {#each c.calls as f}
                  <a href={apiHref(f.formula)}><code>{name(f.formula)}</code></a>
                {/each}
              </span>
            {/each}
          </dd>
        {/if}
        <dt>used in</dt>
        <dd>
          {#each k.uses as u, i}{#if i > 0}; {/if}<a href="#law-{u.law}">{u.short}</a>{#if u.citation}, {u.citation}{/if}{/each}
        </dd>
      </dl>
      {#if k.holds}<p class="muted note">Holds steps of its own.</p>{/if}
      <CodeRef names={[k.qualname]} />
    </section>
  {/each}

  <RefList {references} {statutes} />
{/if}

<style>
  dl {
    display: grid;
    grid-template-columns: max-content minmax(0, 1fr);
    gap: 4px 14px;
    margin: 6px 0 4px;
    font-size: 0.86rem;
  }
  dt {
    color: var(--muted);
  }
  dd {
    margin: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 4px 6px;
  }
  .chain {
    flex-direction: column;
    gap: 4px;
  }
  /* A core concept: plain paper, apart from the step it serves (the drawing's two
     styles); its functions inside it. */
  .concept {
    display: flex;
    flex-direction: column;
    gap: 2px;
    border: 1px solid var(--line);
    border-radius: var(--radius);
    background: var(--surface);
    padding: 4px 8px;
  }
  .concept .name {
    font-weight: 600;
  }
  .fact {
    font-size: 0.8rem;
  }
  .note {
    font-size: 0.82rem;
  }
</style>
