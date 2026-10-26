<script lang="ts">
  // Vote › Lot: ties are results, never decided by sort order; a lot actually drawn is
  // recorded with the vote and decides exactly the tie it was drawn for.
  import type { References } from '../lib/types';
  import CodeRef from './CodeRef.svelte';
  import Law from './Law.svelte';
  import RefList from './RefList.svelte';
  import Term from './Term.svelte';

  export let references: References | null;

  const STATUTES = ['de.st.lwg.2021'] as const;

  const lotsToml = `# election.toml
[[lots]]
section = "erststimme"
unit = "de.st.wk.017"
candidates = ["cdu", "afd"]
winners = ["cdu"]
source = "Niederschrift des Kreiswahlausschusses"`;
</script>

<section>
  <h2>A tie is a result</h2>
  <p>
    Sometimes two claims are exactly equal: two candidates with as many votes in one unit, two
    parties with the same remainder for the last seat. A law that foresees this decides it by
    <b>lot</b>, a <Term t="Losentscheid" />: in the example the winner of a tied
    <Term t="Wahlkreis" /> (<Law id="de.st.lwg.2021">Sec. 33 LWG LSA</Law>) and a seat on equal
    remainders (<Law id="de.st.lwg.2021">Sec. 35 (5) LWG LSA</Law>).
  </p>
  <p>
    The engine never draws, and never lets the order of a list decide either. Where claims are
    equal it returns a <b>tie</b>: the candidates and how many seats they share. A tie is a
    result like any other; what follows it cannot be computed until it is decided, so the next
    step that needs it stops and says which tie it is.
  </p>
  <CodeRef names={['wahlwerk.apportionment.tie.Tie', 'wahlwerk.apportionment.result.Apportionment.with_lot']} />
</section>

<section>
  <h2>The lot as recorded</h2>
  <p>
    A lot that was actually drawn is a fact of the election, as a count is, and it is recorded
    with the vote: where the tie was (its section, its unit), every candidate in it, who won, and
    the record of the draw.
  </p>
  <pre><code>{lotsToml}</code></pre>
  <p>
    The example shows the form, not a draw that happened. A recorded lot decides one tie only:
    the one with the same section and unit, exactly the same candidates and as many seats as it
    has winners. The unit's result keeps the lot, so a seat won by lot says so. When the same
    election is replayed under another law and its ties come out differently, a lot drawn for
    the real tie decides nothing there.
  </p>
  <CodeRef
    names={[
      'wahlwerk.vote.popular.lot.Lot',
      'wahlwerk.process.allocation.elect.SingleMandatePerUnit',
      'wahlwerk.process.allocation.seats.ApportionSeats',
    ]}
  />
</section>

<section>
  <h2>A tie no lot covers</h2>
  <p>
    A tie that arises only in a counterfactual was never drawn for, and the engine does not
    invent a draw: the allocation stops at it. Drawing one at random would make the result
    depend on a seed, and showing one outcome would hide the others.
  </p>
</section>

<RefList {references} statutes={STATUTES} />
