<script lang="ts">
  // Root: loads the numbers build.py derived, then lays out the sections.
  import { onMount } from 'svelte';
  import type { SiteData } from './lib/types';
  import ThemeToggle from './components/ThemeToggle.svelte';
  import Pieces from './components/Pieces.svelte';
  import Protocol from './components/Protocol.svelte';
  import Results from './components/Results.svelte';
  import Hierarchies from './components/Hierarchies.svelte';

  let data: SiteData | null = null;
  let error: string | null = null;

  onMount(async () => {
    try {
      const response = await fetch('data/elections.json');
      if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
      data = (await response.json()) as SiteData;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  });
</script>

<main>
  <header>
    <div class="top">
      <div class="eyebrow">wahlwerk · electoral law as code</div>
      <ThemeToggle />
    </div>
    <h1>From a popular vote to a Landtag</h1>
    <p class="lede">
      wahlwerk turns a tally of votes into a chamber, with the electoral law written as a protocol
      of steps, so a small change to the law can be replayed against real elections. This page
      follows each component, with the Landtage of Sachsen-Anhalt and Mecklenburg-Vorpommern as
      examples.
    </p>
  </header>

  <Pieces />
  <Protocol />

  {#if data}
    <Results elections={data.elections} />
  {:else if error}
    <section><p class="note">The election data could not be loaded: {error}</p></section>
  {:else}
    <section><p class="muted">Loading the elections …</p></section>
  {/if}

  <Hierarchies />

  <footer>
    <p>
      {#if data}Numbers derived by wahlwerk {data.engine}. {/if}
      Engine: <a href="https://github.com/wahlwerk/wahlwerk">wahlwerk/wahlwerk</a> (Apache-2.0) ·
      Site: <a href="https://github.com/wahlwerk/wahlwerk-site">wahlwerk/wahlwerk-site</a> (GPL-3.0) ·
      Election data under its source's licence, named with each result.
    </p>
  </footer>
</main>

<style>
  main {
    max-width: var(--page-width);
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 48px;
  }
  header {
    display: flex;
    flex-direction: column;
    gap: 12px;
    border-bottom: 2px solid var(--ink);
    padding-bottom: 22px;
  }
  .top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
  }
  .lede {
    color: var(--muted);
    font-size: 1.06rem;
  }
  footer {
    border-top: 1px solid var(--line);
    padding-top: 16px;
    font-size: 0.82rem;
    color: var(--muted);
  }
</style>
