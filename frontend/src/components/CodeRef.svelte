<script lang="ts">
  // "In the code": the objects a section describes, each linked to its entry in the
  // API reference, with a link to its source. The reference documents every field and
  // parameter; this page only points there.
  import { apiHref, shortName, sourceHref } from '../lib/api';

  /** Full dotted names, e.g. wahlwerk.vote.popular.tally.TallyRow. */
  export let names: string[];
</script>

<p class="coderef">
  <span class="label">in the code</span>
  {#each names as name, i (name)}
    {#if i > 0}<span class="sep">·</span>{/if}
    <a href={apiHref(name)} title={name}><code>{shortName(name)}</code></a><a
      class="src"
      href={sourceHref(name)}
      title="source on GitHub">src</a
    >
  {/each}
</p>

<style>
  .coderef {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 4px 6px;
    font-size: 0.86rem;
  }
  .label {
    font: 600 0.68rem/1 var(--sans);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-right: 4px;
  }
  .src {
    font: 0.68rem var(--mono);
    color: var(--muted);
    vertical-align: super;
    margin-left: 1px;
  }
  .sep {
    color: var(--muted);
  }
</style>
