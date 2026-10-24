<script lang="ts">
  // The side panel, as in IR-bands: on top the pages of the site, at the bottom the
  // outline of the page shown. Docked beside the column on a wide screen, a drawer
  // below WIDE_MIN_PX (App.svelte opens and closes it).
  //
  // The outline is read from the page itself, its h2 and h3 headings, each given an id
  // if it has none, so it can never disagree with what the page says. It marks the
  // section being read (the last heading scrolled past) and scrolls to a heading
  // without touching the hash, which holds the page route.
  import { createEventDispatcher, onDestroy, tick } from 'svelte';
  import { COMPONENTS, SUBPAGES, href } from '../lib/pages';
  import type { PageId } from '../lib/pages';

  /** The page shown. */
  export let page: PageId;
  /** Changes whenever the page's content may have changed (a page, data arriving). */
  export let contentKey: string;
  /** The element the page renders into. */
  export let content: HTMLElement | null = null;

  const dispatch = createEventDispatcher<{ navigate: void }>();

  interface Heading {
    id: string;
    text: string;
    level: 2 | 3;
  }

  const PAGES: { id: PageId; title: string; note?: string; isSub?: boolean }[] = [
    { id: 'home', title: 'Home' },
    ...COMPONENTS.flatMap((c) => [
      { id: c.id, title: c.title, note: c.role },
      ...SUBPAGES.filter((s) => s.parent === c.id).map((s) => ({ id: s.id, title: s.title, isSub: true })),
    ]),
  ];
  const AFTER: { id: PageId; title: string }[] = [
    { id: 'style', title: 'Style guide' },
    { id: 'impressum', title: 'Impressum' },
  ];

  let headings: Heading[] = [];
  let active = '';
  let observer: IntersectionObserver | null = null;

  function slug(text: string): string {
    return (
      text
        .toLowerCase()
        .normalize('NFKD')
        .replace(/[̀-ͯ]/g, '')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '') || 'section'
    );
  }

  /** A heading's own words, without the badges set beside it ("golden"). */
  function title(h: HTMLHeadingElement): string {
    const copy = h.cloneNode(true) as HTMLElement;
    copy.querySelectorAll('.badge').forEach((b) => b.remove());
    return (copy.textContent ?? '').replace(/\s+/g, ' ').trim();
  }

  async function read(): Promise<void> {
    await tick();
    observer?.disconnect();
    // Home's headings are its cards, one per page: the list above already says them.
    if (!content || page === 'home') {
      headings = [];
      return;
    }
    const used = new Set<string>();
    headings = [...content.querySelectorAll<HTMLHeadingElement>('h2, h3')]
      .filter((h) => !h.closest('[data-outline="skip"]'))
      .map((h) => {
        if (!h.id) {
          let id = `${page}-${slug(title(h))}`;
          for (let n = 2; used.has(id) || document.getElementById(id); n++) id = `${page}-${slug(title(h))}-${n}`;
          h.id = id;
        }
        used.add(h.id);
        return { id: h.id, text: title(h), level: h.tagName === 'H2' ? 2 : 3 };
      });
    active = headings[0]?.id ?? '';
    if (typeof IntersectionObserver === 'undefined') return;
    observer = new IntersectionObserver(spy, { rootMargin: '0px 0px -70% 0px' });
    for (const h of headings) {
      const el = document.getElementById(h.id);
      if (el) observer.observe(el);
    }
  }

  /** The section being read: the last heading above the top 30 % of the window. */
  function spy(): void {
    let current = headings[0]?.id ?? '';
    for (const h of headings) {
      const el = document.getElementById(h.id);
      if (el && el.getBoundingClientRect().top < window.innerHeight * 0.3) current = h.id;
    }
    active = current;
  }

  function go(id: string): void {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    active = id;
    dispatch('navigate');
  }

  $: contentKey, content, void read();
  onDestroy(() => observer?.disconnect());
</script>

<nav class="pages" aria-label="Pages">
  <div class="head">Pages</div>
  <ul>
    {#each PAGES as p (p.id)}
      <li class:sub={p.isSub}>
        <a
          href={href(p.id)}
          class:active={page === p.id}
          aria-current={page === p.id ? 'page' : undefined}
          on:click={() => dispatch('navigate')}
        >
          <span>{p.title}</span>
          {#if p.note}<small>{p.note}</small>{/if}
        </a>
      </li>
    {/each}
  </ul>
  <ul class="minor">
    {#each AFTER as p (p.id)}
      <li>
        <a
          href={href(p.id)}
          class:active={page === p.id}
          aria-current={page === p.id ? 'page' : undefined}
          on:click={() => dispatch('navigate')}>{p.title}</a
        >
      </li>
    {/each}
  </ul>
</nav>

{#if headings.length}
  <nav class="outline" aria-label="On this page">
    <div class="head">On this page</div>
    <ul>
      {#each headings as h (h.id)}
        <li class="l{h.level}">
          <a
            href="#{h.id}"
            class:active={active === h.id}
            aria-current={active === h.id ? 'location' : undefined}
            on:click|preventDefault={() => go(h.id)}>{h.text}</a
          >
        </li>
      {/each}
    </ul>
  </nav>
{/if}

<style>
  li.sub a {
    padding-left: 24px;
  }
  nav {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .head {
    font: 600 0.68rem/1 var(--sans);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    padding: 0 10px;
  }
  ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 1px;
    max-width: none;
  }
  a {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 8px;
    padding: 5px 10px;
    border-left: 2px solid transparent;
    border-radius: 0 var(--radius) var(--radius) 0;
    text-decoration: none;
    color: var(--muted);
    font: 500 0.9rem/1.3 var(--sans);
  }
  a:hover {
    color: var(--ink);
    background: var(--code-bg);
  }
  a.active {
    color: var(--ink);
    border-left-color: var(--accent);
    background: var(--surface);
  }
  small {
    font: 500 0.66rem/1 var(--sans);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
  }
  .minor {
    margin-top: 6px;
    padding-top: 6px;
    border-top: 1px solid var(--line);
  }
  .minor a {
    font-size: 0.82rem;
  }
  /* The cut between the site's menu and the page's own contents. */
  .outline {
    margin-top: 18px;
    padding-top: 16px;
    border-top: 2px solid var(--line);
    min-height: 0;
  }
  .outline a {
    font-size: 0.84rem;
    font-weight: 400;
  }
  .outline .l3 a {
    padding-left: 22px;
    font-size: 0.8rem;
  }
</style>
