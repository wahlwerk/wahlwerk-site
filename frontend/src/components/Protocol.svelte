<script lang="ts">
  // The Law page: a law is a list of steps. Everything about the laws shown here is
  // the engine's (laws.json, written by build.py through laws.py): the steps and their
  // paragraphs, the stages and move ranges derived from what each step reads and writes,
  // and the drawing, made by wahlwerk-ui. The page only explains and shows.
  import type { LawData, Laws, References } from '../lib/types';
  import { href } from '../lib/pages';
  import CodeRef from './CodeRef.svelte';
  import RefList from './RefList.svelte';
  import Term from './Term.svelte';

  export let laws: Laws | null;
  export let references: References | null;

  let chosen = 0;
  $: law = laws ? (laws.laws[chosen] as LawData | undefined) : undefined;
  $: statutes = laws ? laws.laws.map((l) => l.id) : [];

  const F = 'wahlwerk.process.allocation';

  function positions(list: number[]): string {
    return list.length ? list.map((p) => p + 1).join(', ') : 'the tally';
  }

  function range(span: [number, number] | undefined, own: number): string {
    if (!span || span[0] === span[1]) return 'stays';
    return span[0] === own ? `down to ${span[1] + 1}` : span[1] === own ? `up to ${span[0] + 1}` : `${span[0] + 1} to ${span[1] + 1}`;
  }
</script>

<section>
  <h2>A law is a list of steps</h2>
  <div class="prose">
    <p>
      An electoral law, read as a procedure, is a list of <b>steps</b>. Each step is one rule of
      the statute and cites the paragraph it follows: sum the votes per unit, elect the winner of
      each single-seat unit, apply the threshold, set the size of the chamber, apportion the seats.
      The engine calls the list a <b>protocol</b>; a law is a protocol with a name and the dates it
      was in force.
    </p>
    <p>
      The steps work on one record, the <b>allocation</b> (<a href={href('law-allocation')}>Allocation</a>). It starts with the tally of the vote,
      each step adds what it establishes (a sum, the winners, the parties past the threshold, each
      party's seats), and the last step forms the chamber. The allocation is the working record of
      one run of one law on one vote: it is not the law, and it is not kept afterwards.
    </p>
    <p>
      Every step says which <b>facts</b> it reads and which it writes. That is all the structure
      there is: what depends on what, which steps could trade places and what a step needs from
      outside all follow from those two lists, and a law that reads a fact before any step writes it
      is refused when it is written, not halfway through a count.
    </p>
  </div>
  <CodeRef names={['wahlwerk.law.base.Law', `${F}.base.AllocationStep`, `${F}.base.Allocation`, `${F}.base.check_protocol`]} />
</section>

{#if !laws || !law}
  <section><p class="muted">Loading the laws …</p></section>
{:else}
  <div class="tabs" role="tablist" aria-label="Laws" data-outline="skip">
    {#each laws.laws as l, i (l.id)}
      <button role="tab" type="button" aria-selected={i === chosen} class:on={i === chosen} on:click={() => (chosen = i)}>{l.short}</button>
    {/each}
  </div>

  <section>
    <h2>The protocol, drawn</h2>
    <p class="prose">
      The <a href="#law-{law.id}">{law.short}</a> as the engine holds it. Each box is a step with
      the paragraph it follows and its settings; the facts it writes stand in the margin; the number
      in the gutter is its stage. A dashed frame holds steps that act as one: a named
      <b>sequence</b>, or a loop that runs it again. Under a step that computes, the lines
      marked ↳ follow it down to its <b>formula</b>: electing in the
      <Term t="Wahlkreis">Wahlkreise</Term> uses <i>plurality</i>, the most votes win, which is
      one function on the <a href={href('formulas')}>Formulas</a> page; it knows nothing of units
      or parties, so the same choice can serve wherever a law says the most votes win.
    </p>
    <figure class="drawing">{@html law.drawing}</figure>
  </section>

  <section>
    <h2>What depends on what</h2>
    <p class="prose">
      A step depends on the steps that wrote what it reads. Its <b>stage</b> is one more than the
      latest of them, so the steps reading only the tally are stage 0. Stages are a layering, not a
      sorting into kinds: a step can feed several later steps and read from several earlier ones,
      and steps of one stage need nothing of each other. A step can move within the positions
      shown and the law still counts the same, because every step still reads each fact from the
      same writer.
    </p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th class="num">#</th><th>Step</th><th>Follows</th><th class="num">Stage</th><th>Reads from</th><th>Could move</th></tr>
        </thead>
        <tbody>
          {#each law.steps as s, i}
            <tr>
              <td class="num">{i + 1}</td>
              <td>
                <code>{s.kind}</code>
                {#if s.parameters.length}<small>{s.parameters.map(([k, v]) => `${k}=${v}`).join(', ')}</small>{/if}
              </td>
              <td>{s.citation ?? ''}</td>
              <td class="num">{s.stage}</td>
              <td>{positions(s.depends_on)}</td>
              <td>{range(s.movable, i)}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
    <CodeRef names={[`${F}.flow.stages`, `${F}.flow.can_swap`, `${F}.flow.movable`]} />
  </section>

  <section>
    <h2>What the allocation holds</h2>
    <p class="prose">
      The facts of this law's allocation, in the order they are first written, with the steps that
      write and read each. A fact written by a loop is written again each time it runs: the size of
      the chamber is raised and the seats apportioned anew.
    </p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Fact</th><th>Written by</th><th>Read by</th></tr></thead>
        <tbody>
          {#each law.facts as f (f.fact)}
            <tr><td><code>{f.fact}</code></td><td>{f.written.join(', ')}</td><td>{f.read.join(', ') || '·'}</td></tr>
          {/each}
        </tbody>
      </table>
    </div>
  </section>

  <section>
    <h2>Sequences and loops</h2>
    <div class="prose">
      <p>
        Some steps belong together, one feeding the next. The three that take the seats of one
        chamber size, apportion them and deduct the <Term t="Wahlkreis">Wahlkreis</Term> seats are
        one such row; the law names it a <b>sequence</b>, and a sequence is itself a step: it reads
        what its steps need from outside and writes what they write.
      </p>
      <p>
        A <b>loop</b> holds the steps it repeats. When parties win more <Term t="Wahlkreis">Wahlkreise</Term>
        than their share (<Term t="Überhang" />), the loop raises the size of the chamber and runs the
        sequence again, so the sequence is written once even though it runs several times.
      </p>
      <p>
        A number the statute states once is written once: "at least 83 seats" sets the size the
        allocation starts from and the minimum the chamber keeps when the size is raised. Where a
        law gives two numbers, the protocol takes two.
      </p>
    </div>
    <CodeRef names={[`${F}.sequence.StepSequence`, `${F}.mehrsitze.RepeatForMehrsitze`, `${F}.mehrsitze.RaiseForAusgleich`, `${F}.eligibility.SetChamberSize`]} />
  </section>

  <section>
    <h2>Changing a law</h2>
    <div class="prose">
      <p>
        A counterfactual is the same vote under a changed law, and there are two ways to change
        one. <b>Reordering</b> moves a step; it changes nothing as long as every step reads its facts
        from the same writers, and the engine refuses an order in which a step reads a fact before
        it is written. <b>Replacing</b> puts another step, or other settings, in a step's place: another
        apportionment method, another threshold, a loop of another kind, or none. That changes the
        result, which is the point.
      </p>
      <p>
        What each kind of step does, and where each law uses it, is on the
        <a href={href('law-steps')}>Steps</a> page.
      </p>
    </div>
    <CodeRef names={['wahlwerk.law.edit.replace', 'wahlwerk.law.edit.substitute', 'wahlwerk.law.base.Law']} />
  </section>

  <RefList {references} {statutes} />
{/if}

<style>
  .tabs {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin: 4px 0 -8px;
  }
  .tabs button {
    font: 500 0.82rem/1 var(--mono);
    padding: 7px 12px;
    background: var(--surface);
    color: var(--ink);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    cursor: pointer;
  }
  .tabs button.on {
    border-color: var(--accent);
    color: var(--accent);
  }
  .drawing {
    margin: 0;
    overflow-x: auto;
  }
  .drawing :global(svg) {
    display: block;
    max-width: none;
  }
  td small {
    display: block;
    color: var(--muted);
    font-size: 0.78rem;
    overflow-wrap: anywhere;
  }
  .num {
    text-align: right;
  }
</style>
