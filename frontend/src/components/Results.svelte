<script lang="ts">
  // The golden elections: the chamber the engine derives from the votes,
  // equal to the official result. Every number comes from elections.json.
  import type { Election } from '../lib/types';
  import { ELECTION_TEXT } from '../lib/elections';
  import { partyVar } from '../lib/tokens';
  import SeatGrid from './SeatGrid.svelte';

  export let elections: Election[];

  let selected = elections[0]?.key;
  $: election = elections.find((e) => e.key === selected) ?? elections[0];
  $: text = election ? ELECTION_TEXT[election.key] : undefined;

  const count = new Intl.NumberFormat('de-DE');
  const percent = new Intl.NumberFormat('de-DE', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const day = new Intl.DateTimeFormat('de-DE', { day: 'numeric', month: 'long', year: 'numeric' });

  $: seated = election ? election.parties.reduce((s, p) => s + p.votes, 0) : 0;
  $: wahlkreis = election ? election.parties.reduce((s, p) => s + p.wahlkreis, 0) : 0;
</script>

<section>
  <h2>Equal to the official results <span class="badge">golden</span></h2>
  <p>
    Each chamber below is derived from the votes in wahlwerk-data by
    <code>allocate(vote, law.protocol)</code>, in exact fractions, under the law in force on
    election day. The engine's golden tests assert on every run that it equals the official
    Sitzverteilung party by party.
  </p>

  <div class="tabs" role="tablist" aria-label="Election">
    {#each elections as e}
      <button
        role="tab"
        aria-selected={e.key === selected}
        class:active={e.key === selected}
        on:click={() => (selected = e.key)}
      >
        {ELECTION_TEXT[e.key]?.label ?? e.key}
      </button>
    {/each}
  </div>

  {#if election}
    <p class="meta">
      {day.format(new Date(election.date))} · <code>{election.key}</code> · {election.law.title},
      <code>{election.law.id}</code>
    </p>
    <SeatGrid parties={election.parties} />
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Party</th>
            <th class="num">Zweitstimmen</th>
            <th class="num">Share</th>
            <th class="num">Seats</th>
            <th class="num">Wahlkreis</th>
            <th class="num">List</th>
          </tr>
        </thead>
        <tbody>
          {#each election.parties as p}
            <tr>
              <td class="party"><span class="sw" style="--c:{partyVar(p.id)}"></span><span title={p.name}>{p.short_name}</span></td>
              <td class="num">{count.format(p.votes)}</td>
              <td class="num">{percent.format((100 * p.votes) / election.valid_votes)} %</td>
              <td class="num"><b>{p.seats}</b></td>
              <td class="num">{p.wahlkreis}</td>
              <td class="num">{p.list}</td>
            </tr>
          {/each}
          <tr class="others">
            <td>Parties without a seat</td>
            <td class="num">{count.format(election.valid_votes - seated)}</td>
            <td class="num">{percent.format((100 * (election.valid_votes - seated)) / election.valid_votes)} %</td>
            <td class="num">0</td>
            <td class="num"></td>
            <td class="num"></td>
          </tr>
          <tr class="total">
            <td>Total</td>
            <td class="num">{count.format(election.valid_votes)}</td>
            <td class="num">100,0 %</td>
            <td class="num"><b>{election.seats}</b></td>
            <td class="num">{wahlkreis}</td>
            <td class="num">{election.seats - wahlkreis}</td>
          </tr>
        </tbody>
      </table>
    </div>
    {#if text}
      <div class="note">{text.note}</div>
    {/if}
    <p class="source">
      Source: {election.source.publisher},
      {#if election.source.url}<a href={election.source.url}>{election.source.title}</a>{:else}{election.source.title}{/if}.
      {#if election.source.licence}Licence: {election.source.licence}.{/if}
      {#if election.source.attribution}{election.source.attribution}{/if}
    </p>
  {/if}
</section>

<style>
  .tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }
  .tabs button {
    font: 500 0.86rem var(--sans);
    color: var(--muted);
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 6px 11px;
    cursor: pointer;
  }
  .tabs button:hover {
    color: var(--ink);
  }
  .tabs button.active {
    color: var(--ink);
    background: var(--accent-soft);
    border-color: var(--accent);
  }
  .meta {
    font-size: 0.86rem;
    color: var(--muted);
  }
  .sw {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 2px;
    margin-right: 8px;
    background: var(--c);
  }
  td.party {
    white-space: nowrap;
  }
  tr.others td {
    color: var(--muted);
  }
  tr.total td {
    font-weight: 600;
    border-bottom: none;
  }
  .source {
    font-size: 0.8rem;
    color: var(--muted);
  }
</style>
