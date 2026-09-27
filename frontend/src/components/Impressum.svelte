<script lang="ts">
  // Who is responsible for the site, where its numbers come from, and what
  // it does with a visitor's browser.
  import type { Election } from '../lib/types';
  import { ELECTION_TEXT } from '../lib/elections';
  import { OPERATOR } from '../lib/impressum';
  import { href } from '../lib/pages';

  export let elections: Election[];
</script>

<article class="page">
  <header class="page-head">
    <div class="eyebrow">Legal</div>
    <h1>Impressum</h1>
  </header>

  <section>
    <h2>Responsible under § 5 DDG</h2>
    <dl class="info">
      <dt>Name</dt>
      <dd>{OPERATOR.name}</dd>
      {#if OPERATOR.address.length}
        <dt>Address</dt>
        <dd>{#each OPERATOR.address as line, i}{#if i > 0}<br />{/if}{line}{/each}</dd>
      {/if}
      {#if OPERATOR.email}
        <dt>Contact</dt>
        <dd><a href="mailto:{OPERATOR.email}">{OPERATOR.email}</a></dd>
      {/if}
      <dt>Code</dt>
      <dd><a href="https://github.com/wahlwerk">github.com/wahlwerk</a></dd>
    </dl>
  </section>

  <section>
    <h2>About this site</h2>
    <p>
      wahlwerk is an independent project. It is not affiliated with any Landeswahlleitung,
      parliament or party. The seat distributions on this site are derived by the wahlwerk engine
      from published results; its tests check that they equal the official ones. The official
      result of an election is the one its Landeswahlleitung publishes.
    </p>
  </section>

  <section>
    <h2>Data and licences</h2>
    <p>
      The engine and this site are GPL-3.0. The election data comes from wahlwerk-data and
      stays under its source's licence:
    </p>
    {#if elections.length}
      <ul class="sources">
        {#each elections as e}
          <li>
            <b>{ELECTION_TEXT[e.key]?.label ?? e.key}</b>:
            {e.source.publisher},
            {#if e.source.url}<a href={e.source.url}>{e.source.title}</a>{:else}{e.source.title}{/if}.
            {#if e.source.licence}Licence: {e.source.licence}.{/if}
            {#if e.source.attribution}{e.source.attribution}{/if}
          </li>
        {/each}
      </ul>
    {/if}
  </section>

  <section>
    <h2>Privacy</h2>
    <p>
      The site sets no cookies and runs no analytics. Your choice of light or dark theme is kept
      in your own browser's storage and never leaves it. The typefaces are loaded from Google
      Fonts, so your browser sends its IP address to Google when the page loads. The site is
      hosted on GitHub Pages, which logs requests as described in GitHub's privacy statement.
    </p>
  </section>

  <section>
    <h2>Style guide</h2>
    <p>
      How the site looks and why: colour tokens in both themes, party colours, type and layout.
      Every value on that page is read from the token module the site itself uses.
    </p>
    <a class="link-card" href={href('style')}>
      <span class="arrow">→</span>
      <span>
        <b>Open the style guide</b>
        <small>Tokens, type, layout and the rules they follow</small>
        <code>frontend/src/lib/tokens.ts</code>
      </span>
    </a>
  </section>

  <section>
    <h2>Disclaimer</h2>
    <p>
      The content is provided for information, without warranty of any kind. Despite the tests,
      errors in the data or the engine are possible; check against the official publication before
      relying on a number.
    </p>
  </section>
</article>

<style>
  .info {
    display: grid;
    grid-template-columns: 7em minmax(0, 1fr);
    gap: 6px 14px;
    margin: 0;
    font-size: 0.94rem;
  }
  .info dt {
    font-weight: 600;
    color: var(--muted);
  }
  .info dd {
    margin: 0;
    overflow-wrap: anywhere;
  }
  .sources {
    font-size: 0.9rem;
    overflow-wrap: anywhere;
  }
  .link-card {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    max-width: 420px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius-lg);
    padding: 14px 16px;
    color: inherit;
    text-decoration: none;
    transition: box-shadow 0.15s ease, transform 0.12s ease;
  }
  .link-card:hover {
    box-shadow: 0 4px 14px var(--shadow);
    transform: translateY(-2px);
  }
  .link-card .arrow {
    font: 700 1.3rem/1 var(--sans);
    color: var(--accent);
  }
  .link-card span {
    display: flex;
    flex-direction: column;
    gap: 3px;
  }
  .link-card small {
    color: var(--muted);
    font-size: 0.84rem;
  }
  .link-card code {
    align-self: flex-start;
  }
</style>
