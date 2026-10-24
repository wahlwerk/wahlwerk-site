<script lang="ts">
  // A sketch plate: numbered panels, each its art (an SVG from wahlwerk-ui), its title
  // above and its caption below as text. Panels wrap, so a plate works at phone width.
  import type { SketchPlate } from '../lib/types';

  export let plate: SketchPlate;
</script>

<figure class="plate" aria-label={plate.title}>
  <div class="panels">
    {#each plate.panels as p (p.name)}
      <figure class="panel" style="flex-basis:{Math.round(p.width * 0.85)}px">
        <div class="ptitle"><span class="n">{p.number}</span>{p.title}</div>
        <div class="art" style="--w:{Math.round(p.width * 1.15)}px">{@html p.svg}</div>
        <figcaption>
          {#if p.caption.length}<b>{p.caption[0]}</b>{/if}
          {#each p.caption.slice(1) as line}<span>{line}</span>{/each}
        </figcaption>
      </figure>
    {/each}
  </div>
  {#if $$slots.default}<figcaption class="source prose"><slot /></figcaption>{/if}
</figure>

<style>
  .plate {
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  /* The panels of a row share the column's full width: each grows from its drawn width,
     its art centred and scaled up at most 1.15 times, so labels stay near their drawn size. */
  .panels {
    display: flex;
    flex-wrap: wrap;
    gap: 24px 28px;
    align-items: flex-start;
    width: 100%;
  }
  .panel {
    margin: 0;
    flex-grow: 1;
    flex-shrink: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    min-width: 0;
  }
  .ptitle {
    font: 600 0.78rem/1.2 var(--mono);
    color: var(--ink);
  }
  .n {
    color: var(--accent);
    margin-right: 0.6em;
  }
  .art {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  .art :global(svg) {
    width: 100%;
    max-width: var(--w);
    height: auto;
    overflow: visible;
  }
  figcaption {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    font: 0.74rem/1.45 var(--mono);
    color: var(--muted);
  }
  figcaption b {
    font-weight: 600;
    color: var(--ink);
  }
  .source {
    display: block;
    font: 0.82rem/1.5 var(--sans);
    border-top: 1px solid var(--line);
    padding-top: 8px;
  }
</style>
