<script lang="ts">
  // A formula, written in LaTeX in wahlwerk.calc's docstrings and rendered by KaTeX
  // here, as Sphinx renders the same LaTeX in the API reference.
  import katex from 'katex';

  export let tex: string;
  /** A display formula on its own line; inline otherwise. */
  export let display = false;

  $: html = katex.renderToString(tex, { displayMode: display, throwOnError: false, output: 'htmlAndMathml' });
</script>

{#if display}
  <div class="math-display">{@html html}</div>
{:else}
  <span class="math">{@html html}</span>
{/if}

<style>
  .math-display {
    overflow-x: auto;
    overflow-y: hidden;
    padding: 4px 0;
  }
  .math :global(.katex),
  .math-display :global(.katex) {
    font-size: 1.04em;
    color: var(--ink);
  }
</style>
