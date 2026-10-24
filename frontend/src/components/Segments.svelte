<script lang="ts">
  // Running text from a wahlwerk-calc docstring: text, bold, inline formulas, code and
  // citations, as formulas.py split it. A term of art in the text is set as one
  // (Term), so the docstrings need no markup for the site.
  import type { Segment } from '../lib/types';
  import { GLOSSARY } from '../lib/glossary';
  import Math from './Math.svelte';
  import Term from './Term.svelte';
  import Cite from './Cite.svelte';

  export let segments: Segment[];
  /** The page's citer: a BibTeX key to its number. */
  export let cite: (key: string) => number;

  const TERMS = Object.keys(GLOSSARY).sort((a, b) => b.length - a.length);
  const PATTERN = new RegExp(`(?<!\\p{L})(${TERMS.join('|')})((?:e|en|n|s|es)?)(?!\\p{L})`, 'gu');

  type Piece = { text: string } | { term: string; word: string };

  function pieces(text: string): Piece[] {
    const out: Piece[] = [];
    let at = 0;
    for (const match of text.matchAll(PATTERN)) {
      const start = match.index ?? 0;
      if (start > at) out.push({ text: text.slice(at, start) });
      out.push({ term: match[1], word: match[0] });
      at = start + match[0].length;
    }
    if (at < text.length) out.push({ text: text.slice(at) });
    return out;
  }
</script>

{#each segments as s}{#if 'text' in s}{#each pieces(s.text) as p}{#if 'term' in p}<Term t={p.term}
        >{p.word}</Term
      >{:else}{p.text}{/if}{/each}{:else if 'strong' in s}<b>{s.strong}</b>{:else if 'math' in s}<Math
      tex={s.math}
    />{:else if 'code' in s}<code>{s.code}</code>{:else if 'cite' in s}{#each s.cite as key}<Cite
        n={cite(key)}
        {key}
      />{/each}{/if}{/each}
