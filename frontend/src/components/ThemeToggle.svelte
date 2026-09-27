<script lang="ts">
  // Light, dark, or the system's choice. The choice is a per-viewer
  // convenience, remembered in localStorage when the browser allows it.
  import { onMount } from 'svelte';

  type Theme = 'system' | 'light' | 'dark';
  const KEY = 'wahlwerk-theme';
  const NEXT: Record<Theme, Theme> = { system: 'light', light: 'dark', dark: 'system' };

  let theme: Theme = 'system';

  function apply(t: Theme): void {
    if (t === 'system') document.documentElement.removeAttribute('data-theme');
    else document.documentElement.setAttribute('data-theme', t);
  }

  onMount(() => {
    try {
      const saved = localStorage.getItem(KEY);
      if (saved === 'light' || saved === 'dark') theme = saved;
    } catch {
      // storage blocked: stay with the system's choice
    }
    apply(theme);
  });

  function cycle(): void {
    theme = NEXT[theme];
    apply(theme);
    try {
      localStorage.setItem(KEY, theme);
    } catch {
      // storage blocked: the choice lasts for this visit
    }
  }
</script>

<button on:click={cycle} aria-label="Theme: {theme}. Switch theme" title="Theme: {theme}">
  {theme === 'system' ? 'Auto' : theme === 'light' ? 'Light' : 'Dark'}
</button>

<style>
  button {
    font: 500 0.78rem var(--sans);
    color: var(--muted);
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 5px 10px;
    cursor: pointer;
  }
  button:hover {
    color: var(--ink);
  }
</style>
