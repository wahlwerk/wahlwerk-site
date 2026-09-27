<script lang="ts">
  // One square per seat, party by party: solid for a Wahlkreis seat,
  // outlined for a seat from the Landesliste.
  import type { PartyResult } from '../lib/types';
  import { partyVar } from '../lib/tokens';

  export let parties: PartyResult[];

  $: seats = parties.flatMap((p) =>
    Array.from({ length: p.seats }, (_, i) => ({
      color: partyVar(p.id),
      isWahlkreis: i < p.wahlkreis,
      title: `${p.short_name}, ${i < p.wahlkreis ? 'Wahlkreis' : 'Landesliste'}`,
    })),
  );
  $: label = parties.map((p) => `${p.short_name} ${p.seats}`).join(', ');
</script>

<div class="seats" role="img" aria-label="{seats.length} seats: {label}">
  {#each seats as seat}
    <div class="seat" class:list={!seat.isWahlkreis} style="--c:{seat.color}" title={seat.title}></div>
  {/each}
</div>
<div class="legend">
  <span><i></i>solid: won in a Wahlkreis</span>
  <span><i class="list"></i>outlined: from the Landesliste</span>
</div>

<style>
  .seats {
    display: grid;
    grid-template-columns: repeat(21, 1fr);
    gap: 3px;
    max-width: 560px;
  }
  .seat {
    aspect-ratio: 1;
    border-radius: 2px;
    background: var(--c);
  }
  .seat.list {
    background: color-mix(in srgb, var(--c) 40%, var(--surface));
    outline: 1.5px solid var(--c);
    outline-offset: -1.5px;
  }
  .legend {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 18px;
    font-size: 0.84rem;
    color: var(--muted);
  }
  .legend i {
    display: inline-block;
    width: 11px;
    height: 11px;
    border-radius: 2px;
    margin-right: 6px;
    vertical-align: -1px;
    background: var(--muted);
  }
  .legend i.list {
    background: color-mix(in srgb, var(--muted) 40%, var(--surface));
    outline: 1.5px solid var(--muted);
    outline-offset: -1.5px;
  }
</style>
