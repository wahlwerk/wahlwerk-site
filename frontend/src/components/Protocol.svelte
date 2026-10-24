<script lang="ts">
  // The Law page: a law is a list of steps. Everything about the laws shown here is
  // the engine's (laws.json, written by build.py through laws.py): the steps and their
  // paragraphs, the stages and move ranges derived from what each step reads and writes,
  // and the drawing, made by wahlwerk-ui. The page only explains and shows.
  import type { LawData, Laws, References, Sketches } from '../lib/types';
  import { href } from '../lib/pages';
  import { ELECTION_TEXT } from '../lib/elections';
  import CodeRef from './CodeRef.svelte';
  import Plate from './Plate.svelte';
  import RefList from './RefList.svelte';
  import Term from './Term.svelte';

  export let laws: Laws | null;
  export let references: References | null;
  export let sketches: Sketches | null = null;

  $: overhang = law && sketches ? sketches.plates[`overhang-${law.id}`] : undefined;

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
      <b>sequence</b>, or a loop that runs it again.
    </p>
    <p class="prose">
      Two styles keep two things apart. A <b>step</b>, a rule of the law, is drawn in the step
      colour. Inside it, on plain paper, sits each <b>core concept</b> it computes with: a
      method, a threshold, free of any law, with the functions of the
      <a href={href('formulas')}>formulas</a> it calls, and a concept that holds another holds
      its block the same way. A step calls no function itself: whatever it computes, a concept
      it holds computes, even taking the seats won off a number
      (<i>Deduction</i>) or raising a size (<i>Increment</i>). Electing in the <Term t="Wahlkreis">Wahlkreise</Term> is a step;
      under it is <i>plurality</i>, the most votes win, here for one seat; under that, one
      function. Plurality knows nothing of units or parties, so the same concept serves
      wherever a law says the most votes win.
    </p>
    <p class="prose">
      Ink tells what can change. Under each name, faint, is what the step is handed: the facts
      it takes from earlier steps (<code>votes=zweitstimme by land × party</code>), fixed by the
      order of the law. In bold is what can be swapped: a step or a concept as a whole, by its
      name, and each setting the law fixes (<code>seats=83</code>, <code>share=1/20</code>,
      <code>factor=2</code>). Change one of those and the same votes give another chamber.
    </p>
    {#if law.replay}
      <p class="prose">
        Beside each step stands the chamber as the engine had it after that step, its size in
        the middle, counting
        {ELECTION_TEXT[law.replay]?.label ?? law.replay}: hollow seats are not yet anyone's, a
        party's colour solid where a winner of a single-seat unit fills the seat, as an edge
        where a list seat is still to fill. Members a party won beyond its seats stand below the
        floor, outside the chamber, until it is raised for them.
      </p>
    {/if}
    <div class="parts">
      {#each law.parts as part, i}
        <div class="part">
          <figure class="drawing">{@html part.drawing}</figure>
          {#if part.chamber}
            <figure class="state">
              <figcaption class="state-label">after step {i + 1}</figcaption>
              {@html part.chamber}
            </figure>
          {/if}
        </div>
      {/each}
    </div>
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
        The laws here are written in stage order, and each stage is one step or one sequence:
        first what needs nothing but the law and the tally (the size of the chamber, and
        <i>count the votes</i>: the sums per <Term t="Wahlkreis" /> and for the Land), then what
        the counts decide (<i>decide the Wahlkreise and who takes part</i>: each Wahlkreis winner
        and the threshold), then the seats, then the chamber. Inside a stage the order does not
        matter, which the table above shows: the steps of one stage could trade places.
      </p>
      <p>
        A <b>loop</b> holds the steps it repeats and checks, before each round, whether to run
        one: its condition stands in its frame. The seats are allocated once; only when parties
        won more <Term t="Wahlkreis">Wahlkreise</Term> than their share (<Term t="Überhang" />)
        does the loop raise the size of the chamber and allocate again. With no overhang it does
        nothing and the law goes straight on to fill the remaining seats from the lists. The
        sequence is written once even though it runs several times.
      </p>
      <p>
        A number the statute states once is written once: "at least 83 seats" sets the size the
        allocation starts from and the minimum the chamber keeps when the size is raised. Where a
        law gives two numbers, the protocol takes two.
      </p>
    </div>
    <CodeRef names={[`${F}.sequence.StepSequence`, `${F}.overhang.RaiseByOverhang`, `${F}.overhang.RaiseUntilBalanced`, `${F}.eligibility.SetChamberSize`]} />
  </section>

  {#if overhang}
    <section>
      <h2>Raising for overhang, round by round</h2>
      <div class="prose">
        <p>
          A party can win more single-seat units than its share of the votes entitles it to;
          the difference is its <b>overhang</b> (<Term t="Überhang" />). It keeps those seats, so
          the law raises the size of the chamber and divides the seats again until the
          others have caught up, or until its own limit. The first half circle is the chamber
          as allocated before the loop, each next one the chamber after a round, from the
          engine's own rounds of this election: as many seats as the chamber size, each party as many as it is entitled
          to, solid where a unit winner of the party fills it, open where a list seat is
          still to fill. Members a party won in units beyond its seats have no seat yet and
          stand below the floor: the overhang. The next round raises the size and divides
          again, until everyone is seated.
        </p>
        <p>
          The two laws differ only in the loop. The {laws.laws[0].short} raises by twice the
          overhang at once, twice over, and further only while the overhang left exceeds half
          a caucus; the {laws.laws[1]?.short ?? 'other law'} raises one seat at a time, up to
          twice the first overhang, and makes an even chamber odd. Swap the loop and the same
          votes give another chamber: the rest of the law does not change.
        </p>
      </div>
      <Plate plate={overhang} isFull />
      <CodeRef names={[`${F}.overhang.RaiseByOverhang.rounds`, `${F}.overhang.RaiseUntilBalanced.rounds`]} />
    </section>
  {/if}

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
  /* Each step spans the column like the text; the chamber after it stands in the right
     margin, its top level with the step's, where the window has room for it (IR-bands'
     spread). Narrower, the two share the column; at phone width the chamber follows its
     step. */
  .parts {
    container-type: inline-size;
  }
  .part {
    display: grid;
    grid-template-columns: minmax(0, 560fr) minmax(0, 176fr);
    gap: 24px;
    align-items: start;
  }
  .state {
    margin: 0;
  }
  .state-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--muted);
    margin: 8px 0 6px;
    padding-bottom: 4px;
    border-bottom: 1px solid var(--line);
  }
  .state :global(svg) {
    display: block;
    width: 100%;
    height: auto;
  }
  /* Room for the margin: the side panel, its gap, the column and twice the chamber with
     its gap, so the column stays centred (a media query cannot read a token). */
  @media (min-width: 1500px) {
    /* The grid reaches into the margin by the chamber and its gap, so the step keeps the
       column's width and a row is as tall as the taller of the two. */
    .part {
      grid-template-columns: minmax(0, 1fr) 176px;
      gap: 32px;
      margin-right: -208px;
    }
  }
  @container (max-width: 600px) {
    .part {
      grid-template-columns: minmax(0, 1fr);
      gap: 4px;
    }
    /* At its own size, so its labels match the step's, not larger. */
    .state {
      max-width: 176px;
      margin-bottom: 12px;
    }
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
