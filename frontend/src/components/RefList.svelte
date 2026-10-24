<script lang="ts">
  // The sources of a page, in three groups from three homes (lib/citations.ts):
  // literature numbered in the order the page cites it, then the statute versions,
  // then the data. A group the page does not use is left out.
  import { dataHtml, referenceHtml, statuteHtml } from '../lib/citations';
  import type { References } from '../lib/types';

  export let references: References | null;
  /** BibTeX keys, in the order the page cites them. */
  export let literature: readonly string[] = [];
  /** Law ids (one per version) the page cites. */
  export let statutes: readonly string[] = [];
  /** Bundle keys whose numbers the page shows. */
  export let data: readonly string[] = [];
</script>

<section class="refs" aria-labelledby="refs-h">
  <h2 id="refs-h">Sources</h2>
  {#if !references}
    <p class="muted">Loading the sources …</p>
  {:else}
    {#if literature.length}
      <h3>Literature</h3>
      <ol>
        {#each literature as key (key)}
          <li class="prose" id="ref-{key}">{@html referenceHtml(references.literature[key], key)}</li>
        {/each}
      </ol>
    {/if}
    {#if statutes.length}
      <h3>Statutes</h3>
      <ul>
        {#each statutes as id (id)}
          <li class="prose" id="law-{id}">{@html statuteHtml(references.statutes[id], id)}</li>
        {/each}
      </ul>
    {/if}
    {#if data.length}
      <h3>Data</h3>
      <ul>
        {#each data as key (key)}
          <li class="prose" id="data-{key}">{@html dataHtml(references.data[key], key)}</li>
        {/each}
      </ul>
    {/if}
  {/if}
</section>

<style>
  .refs h3 {
    font: 600 0.72rem/1 var(--sans);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 6px;
  }
  .refs ol,
  .refs ul {
    font-size: 0.86rem;
    color: var(--muted);
    gap: 6px;
    overflow-wrap: anywhere;
  }
  /* Sources are set like the text above them: full column, justified (.prose), markers
     hanging outside the column. */
  .refs ol,
  .refs ul {
    padding-left: 0;
    list-style-position: outside;
  }
  @media (max-width: 599px) {
    .refs ol,
    .refs ul {
      padding-left: 1.2em;
    }
  }
  .refs li :global(em) {
    color: var(--ink);
  }
  .refs li :global(.missing) {
    color: var(--accent);
  }
</style>
