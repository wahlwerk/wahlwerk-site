<script lang="ts">
  // One symbol per component, drawn in currentColor so the caller picks the
  // colour from a token.
  import type { ComponentId } from '../lib/pages';

  export let name: ComponentId;
  export let size = 26;
</script>

<svg
  width={size}
  height={size}
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.8"
  stroke-linecap="round"
  stroke-linejoin="round"
  aria-hidden="true"
>
  {#if name === 'vote'}
    <!-- a ballot going into the box -->
    <path d="M8 12V4h8v8" />
    <path d="M10.5 7h3" />
    <path d="M3.5 12h17v8h-17z" />
    <path d="M9 15.5h6" />
  {:else if name === 'law'}
    <!-- an ordered list of steps -->
    <path d="M9.5 6h10M9.5 12h10M9.5 18h10" />
    <path d="M4.5 5l1-1v4M4 11.5a1 1 0 0 1 2 .3L4 14h2M4 17h2l-1 1.2a1 1 0 1 1-1 1.3" />
  {:else if name === 'allocation'}
    <!-- one record, split into seats -->
    <path d="M3 12h6" />
    <circle cx="10.5" cy="12" r="1.5" />
    <path d="M12 11l7-5M12 12h7M12 13l7 5" />
  {:else}
    <!-- a hemicycle -->
    <path d="M3 19a9 9 0 0 1 18 0" />
    <path d="M7.5 19a4.5 4.5 0 0 1 9 0" />
    <path d="M2.5 19h19" />
  {/if}
</svg>
