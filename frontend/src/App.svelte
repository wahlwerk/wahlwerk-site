<script lang="ts">
  // Root: loads the numbers build.py derived, follows the location hash to a
  // page, and frames it with the top bar and the footer.
  import { onMount } from 'svelte';
  import type { Formulas as FormulasData, Laws, References, SiteData, Sketches } from './lib/types';
  import { COMPONENTS, SUBPAGES, href, pageFromHash } from './lib/pages';
  import type { PageId } from './lib/pages';
  import ThemeToggle from './components/ThemeToggle.svelte';
  import Sidebar from './components/Sidebar.svelte';
  import Home from './components/Home.svelte';
  import Vote from './components/Vote.svelte';
  import Protocol from './components/Protocol.svelte';
  import Pieces from './components/Pieces.svelte';
  import Results from './components/Results.svelte';
  import Formulas from './components/Formulas.svelte';
  import Steps from './components/Steps.svelte';
  import Impressum from './components/Impressum.svelte';
  import StyleGuide from './components/StyleGuide.svelte';

  let data: SiteData | null = null;
  let sketches: Sketches | null = null;
  let references: References | null = null;
  let formulas: FormulasData | null = null;
  let laws: Laws | null = null;
  let error: string | null = null;
  let page: PageId = pageFromHash(window.location.hash);

  $: index = COMPONENTS.findIndex((c) => c.id === page);
  $: component = index >= 0 ? COMPONENTS[index] : null;
  $: prev = index > 0 ? COMPONENTS[index - 1] : null;
  $: next = index >= 0 && index < COMPONENTS.length - 1 ? COMPONENTS[index + 1] : null;

  /** The page's own element, read by the side panel for its outline. */
  let content: HTMLElement | null = null;
  /** Below WIDE_MIN_PX the side panel is a drawer, closed until the menu button opens it. */
  let drawerOpen = false;
  $: contentKey = `${page}:${data ? 1 : 0}:${sketches ? 1 : 0}:${references ? 1 : 0}:${formulas ? 1 : 0}:${laws ? 1 : 0}`;
  $: subpage = SUBPAGES.find((s) => s.id === page) ?? null;
  $: parent = subpage ? COMPONENTS.find((c) => c.id === subpage?.parent) ?? null : null;

  function follow(): void {
    const id = window.location.hash.replace(/^#\/?/, '');
    // A link to a place on the page (#law-de.bund.gg, #ref-key) is not a route: put the
    // route back and scroll there, so the page shown stays the page shown.
    if (window.location.hash && !window.location.hash.startsWith('#/') && document.getElementById(id)) {
      history.replaceState(null, '', href(page));
      document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
    page = pageFromHash(window.location.hash);
    drawerOpen = false;
    window.scrollTo(0, 0);
  }

  function key(event: KeyboardEvent): void {
    if (event.key === 'Escape') drawerOpen = false;
  }

  async function json<T>(path: string): Promise<T> {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`${path}: ${response.status} ${response.statusText}`);
    return (await response.json()) as T;
  }

  async function load(): Promise<void> {
    try {
      [data, sketches, references, formulas, laws] = await Promise.all([
        json<SiteData>('data/elections.json'),
        json<Sketches>('data/sketches.json'),
        json<References>('data/references.json'),
        json<FormulasData>('data/formulas.json'),
        json<Laws>('data/laws.json'),
      ]);
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    }
  }

  onMount(() => {
    window.addEventListener('hashchange', follow);
    window.addEventListener('keydown', key);
    void load();
    return () => {
      window.removeEventListener('hashchange', follow);
      window.removeEventListener('keydown', key);
    };
  });
</script>

<header class="bar">
  <button
    class="menu"
    type="button"
    on:click={() => (drawerOpen = !drawerOpen)}
    aria-expanded={drawerOpen}
    aria-controls="sidebar"
    aria-label={drawerOpen ? 'Close the side panel' : 'Open the side panel'}>{drawerOpen ? '✕' : '☰'}</button
  >
  <a class="brand" href={href('home')} aria-current={page === 'home' ? 'page' : undefined}>wahlwerk</a>
  <ThemeToggle />
</header>

<div class="shell">
  {#if drawerOpen}
    <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
    <div class="backdrop" on:click={() => (drawerOpen = false)}></div>
  {/if}
  <aside id="sidebar" class="sidebar" class:open={drawerOpen} aria-label="Side panel">
    <Sidebar {page} {contentKey} {content} on:navigate={() => (drawerOpen = false)} />
  </aside>


<main class:wide={page === 'home'} bind:this={content}>
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
        <Vote {sketches} {references} />
      {:else if page === 'law'}
        <Protocol {laws} {references} />
      {:else if page === 'allocation'}
        <Pieces />
      {:else if page === 'formulas'}
        <Formulas {formulas} {references} />
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
  {:else if subpage && parent}
    <article class="page">
      <header class="page-head">
        <div class="eyebrow"><a href={href(parent.id)}>{parent.title}</a> · {subpage.title}</div>
        <h1>{subpage.title}</h1>
        <p class="lede">Every kind of step the laws on this site are made of: what it does, what it reads and writes, and where each law uses it.</p>
      </header>
      {#if page === 'law-steps'}
        <Steps {laws} {references} />
      {/if}
      <nav class="steps" aria-label="Back">
        <a href={href(parent.id)}><small>← {parent.role}</small>{parent.title}</a>
      </nav>
    </article>
  {:else if page === 'impressum'}
    <Impressum elections={data?.elections ?? []} />
  {:else if page === 'style'}
    <StyleGuide {sketches} />
  {/if}
</main>
</div>

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
  /* The shell: the top bar across, then the side panel beside the page, then the
     footer. From WIDE_MIN_PX (1080 px; a media query cannot read a token) the panel is
     docked and sticky; below it, it is a drawer over the page, opened by the menu
     button. */
  .bar,
  .shell,
  footer {
    max-width: calc(var(--sidebar-width) + 48px + var(--wide-width));
    margin-inline: auto;
  }
  .bar {
    display: flex;
    align-items: center;
    gap: 10px 16px;
    padding: 16px 0 14px;
    border-bottom: 2px solid var(--ink);
  }
  .brand {
    font: 650 1.25rem/1 var(--serif);
    text-decoration: none;
  }
  .bar :global(button:last-child) {
    margin-left: auto;
  }
  .menu {
    font: 500 1.1rem/1 var(--sans);
    width: 34px;
    height: 34px;
    display: grid;
    place-items: center;
    background: none;
    color: var(--ink);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    cursor: pointer;
  }

  .shell {
    display: grid;
    grid-template-columns: var(--sidebar-width) minmax(0, 1fr);
    gap: 48px;
  }
  .sidebar {
    position: sticky;
    top: 0;
    align-self: start;
    max-height: 100dvh;
    overflow-y: auto;
    padding: 36px 4px 24px 0;
  }
  .backdrop {
    display: none;
  }
  @media (min-width: 1080px) {
    .menu {
      display: none;
    }
  }
  @media (max-width: 1079px) {
    .shell {
      display: block;
    }
    .sidebar {
      position: fixed;
      z-index: 20;
      top: 0;
      left: 0;
      bottom: 0;
      height: 100dvh;
      width: min(280px, 85vw);
      max-height: none;
      padding: 20px 14px;
      background: var(--bg);
      border-right: 1px solid var(--line);
      box-shadow: 0 0 24px var(--shadow);
      transform: translateX(-105%);
      transition: transform 0.18s ease;
    }
    .sidebar.open {
      transform: none;
    }
    .backdrop {
      display: block;
      position: fixed;
      z-index: 19;
      inset: 0;
      background: var(--shadow);
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .sidebar {
      transition: none;
    }
  }

  main.wide {
    max-width: var(--wide-width);
  }
  main {
    max-width: var(--page-width);
    margin: 0 auto;
    padding-top: 36px;
    min-width: 0;
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
