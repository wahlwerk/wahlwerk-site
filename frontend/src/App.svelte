<script lang="ts">
  // Root: loads the numbers build.py derived, follows the location hash to a
  // page, and frames it with the top bar and the footer.
  import { onMount } from 'svelte';
  import type { SiteData } from './lib/types';
  import { COMPONENTS, href, pageFromHash } from './lib/pages';
  import type { PageId } from './lib/pages';
  import ThemeToggle from './components/ThemeToggle.svelte';
  import Home from './components/Home.svelte';
  import Hierarchies from './components/Hierarchies.svelte';
  import Protocol from './components/Protocol.svelte';
  import Pieces from './components/Pieces.svelte';
  import Results from './components/Results.svelte';
  import Impressum from './components/Impressum.svelte';
  import StyleGuide from './components/StyleGuide.svelte';

  let data: SiteData | null = null;
  let error: string | null = null;
  let page: PageId = pageFromHash(window.location.hash);

  $: index = COMPONENTS.findIndex((c) => c.id === page);
  $: component = index >= 0 ? COMPONENTS[index] : null;
  $: prev = index > 0 ? COMPONENTS[index - 1] : null;
  $: next = index >= 0 && index < COMPONENTS.length - 1 ? COMPONENTS[index + 1] : null;

  function follow(): void {
    page = pageFromHash(window.location.hash);
    window.scrollTo(0, 0);
  }

  async function load(): Promise<void> {
    try {
      const response = await fetch('data/elections.json');
      if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
      data = (await response.json()) as SiteData;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  onMount(() => {
    window.addEventListener('hashchange', follow);
    void load();
    return () => window.removeEventListener('hashchange', follow);
  });
</script>

<header class="bar">
  <a class="brand" href={href('home')} aria-current={page === 'home' ? 'page' : undefined}>wahlwerk</a>
  <nav aria-label="Components">
    {#each COMPONENTS as c}
      <a href={href(c.id)} class:active={page === c.id} aria-current={page === c.id ? 'page' : undefined}>{c.title}</a>
    {/each}
  </nav>
  <ThemeToggle />
</header>

<main class:wide={page === 'home'}>
  {#if page === 'home'}
    <Home {data} />
  {:else if component}
    <article class="page">
      <header class="page-head">
        <div class="eyebrow">{index + 1} of {COMPONENTS.length} · {component.role}</div>
        <h1>{component.title}</h1>
        <p class="lede">{component.lede}</p>
      </header>

      {#if page === 'vote'}
        <Hierarchies />
      {:else if page === 'law'}
        <Protocol />
      {:else if page === 'allocation'}
        <Pieces />
      {:else if data}
        <Results elections={data.elections} />
      {:else if error}
        <section><p class="note">The election data could not be loaded: {error}</p></section>
      {:else}
        <section><p class="muted">Loading the elections …</p></section>
      {/if}

      <nav class="steps" aria-label="Previous and next component">
        {#if prev}
          <a href={href(prev.id)}><small>← {prev.role}</small>{prev.title}</a>
        {:else}
          <span></span>
        {/if}
        {#if next}
          <a class="next" href={href(next.id)}><small>{next.role} →</small>{next.title}</a>
        {/if}
      </nav>
    </article>
  {:else if page === 'impressum'}
    <Impressum elections={data?.elections ?? []} />
  {:else if page === 'style'}
    <StyleGuide />
  {/if}
</main>

<footer>
  <p>
    {#if data}Numbers derived by wahlwerk {data.engine}. {/if}
    Engine: <a href="https://github.com/wahlwerk/wahlwerk">wahlwerk/wahlwerk</a> (GPL-3.0) ·
    Site: <a href="https://github.com/wahlwerk/wahlwerk-site">wahlwerk/wahlwerk-site</a> (GPL-3.0) ·
    Election data under its source's licence, named with each result.
  </p>
  <p class="links">
    <a href={href('impressum')}>Impressum</a>
    <a href={href('style')}>Style guide</a>
  </p>
</footer>

<style>
  .bar,
  main.wide,
  footer {
    max-width: var(--wide-width);
  }
  .bar {
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px 20px;
    padding: 16px 0 14px;
    border-bottom: 2px solid var(--ink);
  }
  .brand {
    font: 650 1.25rem/1 var(--serif);
    text-decoration: none;
  }
  .bar nav {
    display: flex;
    flex-wrap: wrap;
    gap: 4px 18px;
    flex: 1;
    order: 2;
  }
  .bar :global(button) {
    order: 1;
    margin-left: auto;
  }
  @media (min-width: 600px) {
    .bar nav { order: 0; }
    .bar :global(button) { order: 0; }
  }
  @media (max-width: 599px) {
    .bar nav { flex-basis: 100%; }
  }
  .bar nav a {
    font: 500 0.9rem var(--sans);
    color: var(--muted);
    text-decoration: none;
    padding: 4px 0;
    border-bottom: 2px solid transparent;
  }
  .bar nav a:hover {
    color: var(--ink);
  }
  .bar nav a.active {
    color: var(--ink);
    border-bottom-color: var(--accent);
  }

  main {
    max-width: var(--page-width);
    margin: 0 auto;
    padding-top: 36px;
  }

  .steps {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    border-top: 1px solid var(--line);
    padding-top: 18px;
  }
  .steps a {
    display: flex;
    flex-direction: column;
    gap: 2px;
    font: 650 1.05rem/1.2 var(--serif);
    text-decoration: none;
  }
  .steps a:hover {
    color: var(--accent);
  }
  .steps small {
    font: 600 0.68rem/1 var(--sans);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
  }
  .steps .next {
    text-align: right;
    align-items: flex-end;
  }

  footer {
    margin: 64px auto 0;
    border-top: 1px solid var(--line);
    padding-top: 16px;
    font-size: 0.82rem;
    color: var(--muted);
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  footer .links {
    display: flex;
    gap: 18px;
  }
</style>
