<script lang="ts">
  // The front door: what wahlwerk is, how much the site reproduces, and one
  // card per component in the order the engine runs them.
  import type { SiteData } from '../lib/types';
  import { COMPONENTS, href } from '../lib/pages';
  import Icon from './Icon.svelte';

  export let data: SiteData | null;

  const count = new Intl.NumberFormat('de-DE');

  // Totals over what build.py derived; nothing here is apportioned.
  $: elections = data?.elections ?? [];
  $: laws = new Set(elections.map((e) => e.law.id)).size;
  $: seats = elections.reduce((s, e) => s + e.seats, 0);
</script>

<div class="home">
  <div class="hero">
    <h1>wahlwerk</h1>
    <p class="tagline">Electoral law as code · from a popular vote to a Landtag</p>
    <p class="desc">
      wahlwerk turns a tally of votes into a chamber, with the electoral law written as a
      protocol of steps, so a change to the law can be replayed against real elections. This
      site follows each component in turn, using elections the engine reproduces exactly.
    </p>
  </div>

  {#if elections.length}
    <!-- How much the engine reproduces, before anything is clicked. -->
    <div class="scope">
      <div class="stat">
        <span class="n">{elections.length}</span>
        <span class="l">golden elections</span>
      </div>
      <div class="stat">
        <span class="n">{laws}</span>
        <span class="l">electoral laws</span>
      </div>
      <div class="stat">
        <span class="n">{count.format(seats)}</span>
        <span class="l">seats derived</span>
      </div>
    </div>
  {/if}

  <nav class="cards" aria-label="Components">
    {#each COMPONENTS as c, i}
      <a class="card" href={href(c.id)}>
        <span class="icon"><Icon name={c.id} /></span>
        <span class="role">{i + 1} · {c.role}</span>
        <h2>{c.title}</h2>
        <p>{c.card}</p>
        <span class="cta">Open {c.title.toLowerCase()} →</span>
      </a>
    {/each}
  </nav>

  <p class="what">
    It covers the Landtage of Sachsen-Anhalt and Mecklenburg-Vorpommern: Wahlkreise won by
    Erststimme, seats apportioned by Zweitstimme above the threshold, and the Überhang and
    Ausgleich that follow when a party wins more Wahlkreise than its share.
  </p>
</div>

<style>
  .home {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 28px;
  }

  .hero {
    text-align: center;
    max-width: 600px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    margin-bottom: 34px;
  }
  h1 {
    font-size: clamp(2.3rem, 7vw, 3.1rem);
    letter-spacing: -0.015em;
  }
  .tagline {
    font-family: var(--serif);
    font-style: italic;
    color: var(--muted);
    margin-bottom: 6px;
  }
  .desc {
    font-size: 0.98rem;
    line-height: 1.65;
  }

  /* Three numbers, large, above the cards: the size of the thing is the
     second fact about it after what it is. */
  .scope {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 14px 56px;
    margin-bottom: 40px;
  }
  .stat {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
  }
  .stat .n {
    font: 650 2.3rem/1.1 var(--serif);
    font-variant-numeric: tabular-nums;
  }
  .stat .l {
    font: 500 0.72rem/1.2 var(--sans);
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: var(--muted);
  }

  /* Four components in one row where there is room, 2x2 below that, then a
     stack: the flow reads left to right, then top to bottom. */
  .cards {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 20px;
    width: 100%;
  }
  @media (max-width: 960px) {
    .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); max-width: 720px; }
  }
  @media (max-width: 520px) {
    .cards { grid-template-columns: 1fr; max-width: 380px; }
  }

  .card {
    display: flex;
    flex-direction: column;
    gap: 10px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-lg);
    padding: 24px 20px 20px;
    color: inherit;
    text-decoration: none;
    transition: box-shadow 0.18s ease, transform 0.15s ease, border-color 0.18s ease;
  }
  .card:hover {
    box-shadow: 0 6px 22px var(--shadow);
    transform: translateY(-3px);
    border-color: var(--accent);
  }
  .icon {
    width: 50px;
    height: 50px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--accent-soft);
    color: var(--ink);
    margin-bottom: 4px;
  }
  .role {
    font: 600 0.68rem/1 var(--sans);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent);
  }
  .card h2 {
    font-size: 1.3rem;
  }
  .card p {
    font-size: 0.88rem;
    line-height: 1.5;
    color: var(--muted);
    flex: 1;
  }
  .cta {
    font: 600 0.84rem var(--sans);
    color: var(--accent);
  }

  .what {
    max-width: 680px;
    text-align: center;
    font-size: 0.88rem;
    color: var(--muted);
    margin-top: 34px;
  }
</style>
