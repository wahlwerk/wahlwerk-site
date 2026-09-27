<script lang="ts">
  // The design system, read from lib/tokens.ts: nothing on this page is a
  // second copy of a value, so it cannot drift from what the site uses.
  import { COLORS, PARTY_COLORS, FONTS, LAYOUT } from '../lib/tokens';
  import type { ColorToken } from '../lib/tokens';

  const colors = Object.entries(COLORS);
  const parties = Object.entries(PARTY_COLORS);
  const fonts = Object.entries(FONTS);
  const layout = Object.entries(LAYOUT);

  const FONT_ROLE: Record<string, string> = {
    serif: 'Headings, the home title, large numbers',
    sans: 'Body text, labels, controls',
    mono: 'Code, protocol steps, legal citations',
  };

  const rules = [
    ['Every number from the engine', 'Seats, votes and shares come from elections.json, which build.py derives through wahlwerk. The page never apportions and never hard-codes a result.'],
    ['Tokens only', 'No component hard-codes a colour, font or radius. A new value is a new token in lib/tokens.ts, with a usage note.'],
    ['Both themes', 'Every colour has a light and a dark value. The toggle cycles auto, light and dark.'],
    ['Party colours are data', 'A party colour encodes a party in a seat grid or a swatch, and nothing else. Chrome uses the gold accent.'],
    ['Phone width', 'Every page works at 390 px with a 16 px gutter and no sideways page scroll; wide tables scroll inside their own box.'],
    ['Sources are named', 'Every result shows its publisher, title, licence and attribution.'],
    ['Language', 'English prose, German terms of art: Wahlkreis, Zweitstimme, Überhang. No em-dashes.'],
  ];

  function pair(t: ColorToken): string {
    return `${t.light} / ${t.dark}`;
  }
</script>

<article class="page">
  <header class="page-head">
    <div class="eyebrow">Design</div>
    <h1>Style guide</h1>
    <p class="lede">
      Warm paper, near-black ink and one gold accent; Literata for headings, IBM Plex for text and
      code. Every value below is read from <code>frontend/src/lib/tokens.ts</code>.
    </p>
  </header>

  <section>
    <h2>Colour tokens</h2>
    <p class="muted">Each swatch shows the light value on the left and the dark value on the right.</p>
    <ul class="swatches">
      {#each colors as [name, t]}
        <li>
          <span class="chip" style="--l:{t.light}; --d:{t.dark}"><i></i><i></i></span>
          <span class="meta">
            <code>--{name}</code>
            <small>{t.usage}</small>
            <small class="hex">{pair(t)}</small>
          </span>
        </li>
      {/each}
    </ul>
  </section>

  <section>
    <h2>Party colours</h2>
    <p class="muted">
      Keyed by the party id the engine uses; a party without its own colour falls back to
      <code>--party-party-other</code>.
    </p>
    <ul class="swatches">
      {#each parties as [id, t]}
        <li>
          <span class="chip" style="--l:{t.light}; --d:{t.dark}"><i></i><i></i></span>
          <span class="meta">
            <code>--party-{id}</code>
            <small>{t.usage}</small>
            <small class="hex">{pair(t)}</small>
          </span>
        </li>
      {/each}
    </ul>
  </section>

  <section>
    <h2>Typefaces</h2>
    <div class="fonts">
      {#each fonts as [name, stack]}
        <div class="font">
          <div class="sample" style="font-family: var(--{name})">Zweitstimmen 1 234 567 · § 35 (8)</div>
          <code>--{name}</code>
          <small>{FONT_ROLE[name] ?? ''}</small>
          <small class="hex">{stack}</small>
        </div>
      {/each}
    </div>
  </section>

  <section>
    <h2>Type in use</h2>
    <div class="specimens">
      <div class="row"><span class="tag">h1</span><h1>From a vote to a Landtag</h1></div>
      <div class="row"><span class="tag">h2</span><h2>An electoral law as a protocol</h2></div>
      <div class="row"><span class="tag">h3</span><h3>Main: in the ids</h3></div>
      <div class="row"><span class="tag">lede</span><p class="lede">One sentence under a page title, in the muted ink.</p></div>
      <div class="row"><span class="tag">body</span><p>Body text at 16 px on a line height of 1.6, at most 68 characters wide.</p></div>
      <div class="row"><span class="tag">.eyebrow</span><div class="eyebrow">wahlwerk · electoral law as code</div></div>
      <div class="row"><span class="tag">code</span><p>Call <code>allocate(vote, law.protocol)</code>.</p></div>
      <div class="row"><span class="tag">.law</span><span class="law">§ 35 (5), (6)</span></div>
      <div class="row"><span class="tag">.badge</span><span><span class="badge">golden</span></span></div>
      <div class="row"><span class="tag">.note</span><div class="note">A note says what is special about one result under its law.</div></div>
    </div>
  </section>

  <section>
    <h2>Layout</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Token</th><th>Value</th></tr></thead>
        <tbody>
          {#each layout as [name, value]}
            <tr><td><code>--{name}</code></td><td class="num">{value}</td></tr>
          {/each}
        </tbody>
      </table>
    </div>
  </section>

  <section>
    <h2>Rules</h2>
    <dl class="rules">
      {#each rules as [head, text]}
        <dt>{head}</dt>
        <dd>{text}</dd>
      {/each}
    </dl>
  </section>
</article>

<style>
  .swatches {
    list-style: none;
    padding: 0;
    max-width: none;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 10px;
  }
  .swatches li {
    display: flex;
    gap: 12px;
    align-items: center;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 10px;
    min-width: 0;
  }
  .chip {
    display: flex;
    flex-shrink: 0;
    border: 1px solid var(--line);
    border-radius: var(--radius);
    overflow: hidden;
  }
  .chip i {
    display: block;
    width: 26px;
    height: 44px;
    background: var(--l);
  }
  .chip i + i {
    background: var(--d);
  }
  .meta {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
  }
  .meta code {
    align-self: flex-start;
  }
  .meta small {
    font-size: 0.8rem;
    color: var(--muted);
    line-height: 1.35;
  }
  .hex {
    font-family: var(--mono);
    overflow-wrap: anywhere;
  }

  .fonts {
    display: grid;
    gap: 10px;
  }
  .font {
    display: flex;
    flex-direction: column;
    gap: 4px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 12px 14px;
  }
  .font .sample {
    font-size: 1.3rem;
    overflow-wrap: anywhere;
  }
  .font code {
    align-self: flex-start;
  }
  .font small {
    font-size: 0.8rem;
    color: var(--muted);
  }

  .specimens {
    display: flex;
    flex-direction: column;
    border-top: 1px solid var(--line);
  }
  .row {
    display: grid;
    grid-template-columns: 6em minmax(0, 1fr);
    gap: 12px;
    align-items: baseline;
    padding: 12px 0;
    border-bottom: 1px solid var(--line);
  }
  .tag {
    font: 500 0.78rem var(--mono);
    color: var(--muted);
  }

  .rules {
    margin: 0;
    display: grid;
    grid-template-columns: minmax(8em, 13em) minmax(0, 1fr);
    gap: 10px 18px;
    max-width: 68ch;
  }
  .rules dt {
    font-weight: 600;
  }
  .rules dd {
    margin: 0;
    color: var(--muted);
    font-size: 0.94rem;
  }
  @media (max-width: 560px) {
    .rules { grid-template-columns: 1fr; gap: 2px; }
    .rules dd { margin-bottom: 10px; }
    .row { grid-template-columns: 1fr; gap: 4px; }
  }
</style>
