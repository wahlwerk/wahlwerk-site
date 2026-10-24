<script lang="ts">
  // A sketch plate: numbered panels, each its art (an SVG from wahlwerk-ui), its title
  // above and its caption below as text. Panels wrap, so a plate works at phone width.
  import type { SketchPlate } from '../lib/types';

  export let plate: SketchPlate;
  /** The panels fill the column, in equal columns, their art scaled up to the width:
   * for a plate that is the figure of its section rather than a row of small sketches. */
  export let isFull = false;
</script>

<figure class="plate" aria-label={plate.title}>
  <div class="panels" class:full={isFull}>
    {#each plate.panels as p (p.name)}
      <figure class="panel" style="flex-basis:{Math.round(p.width * 0.85)}px">
        <div class="ptitle"><span class="n">{p.number}</span>{p.title}</div>
        <div class="art" style="--w:{Math.round(p.width * 1.15)}px">
          <div class="frame">
            {@html p.svg}
            <!-- Links over the art (sketches.py places them): the drawing stays code, the
                 page only makes its boxes reachable. Later links sit on top of earlier ones. -->
            {#each p.links ?? [] as l}
              <a
                class="hit"
                href={l.href}
                aria-label={l.label}
                title={l.label}
                style="left:{(100 * l.x) / p.width}%;top:{(100 * l.y) / p.height}%;width:{(100 * l.w) / p.width}%;height:{(100 * l.h) / p.height}%"
              ></a>
            {/each}
          </div>
        </div>
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
  /* Full width: equal columns of at least 200 px, so three sit in a row of the column
     and a phone shows one; the art fills its column, whatever its drawn width. */
  .panels.full {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
  .panels.full .frame {
    max-width: none;
  }
  .frame {
    position: relative;
    width: 100%;
    max-width: var(--w);
  }
  .frame :global(svg) {
    display: block;
    width: 100%;
    height: auto;
    overflow: visible;
  }
  .hit {
    position: absolute;
    border-radius: var(--radius);
    outline: 1px solid transparent;
    transition: outline-color 0.15s ease;
  }
  .hit:hover,
  .hit:focus-visible {
    outline-color: var(--accent);
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
