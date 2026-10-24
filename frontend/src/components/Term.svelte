<script lang="ts">
  // A term of art: the name one system gives to a concept (Landtag for a chamber,
  // Wahlkreis for a unit). Italic, dotted underline; hovering it says which
  // concept it is and in which system (lib/glossary.ts). The slot is the word as the
  // sentence needs it (a plural, a case); without one, the term itself.
  import { termTitle } from '../lib/glossary';

  /** The glossary entry. */
  export let t: string;
</script>

<span class="term" title={termTitle(t)}><slot>{t}</slot></span>

<style>
  .term {
    font-style: italic;
    text-decoration: underline dotted;
    text-decoration-color: var(--muted);
    text-decoration-thickness: 1px;
    text-underline-offset: 3px;
    cursor: help;
  }
</style>
