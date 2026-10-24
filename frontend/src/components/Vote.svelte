<script lang="ts">
  // The Vote page: what a vote is, who votes, what is voted on and what is recorded,
  // each with a plate of sketches (drawn by build.py with wahlwerk-ui from a real
  // bundle), links into the API reference, and the sources at the foot.
  import type { References, Sketches } from '../lib/types';
  import Plate from './Plate.svelte';
  import CodeRef from './CodeRef.svelte';
  import Law from './Law.svelte';
  import RefList from './RefList.svelte';
  import Hierarchies from './Hierarchies.svelte';

  export let sketches: Sketches | null;
  export let references: References | null;

  const STATUTES = ['de.bund.gg', 'de.bund.gobt'] as const;
  const DATA = ['de.landtag.st.2026'] as const;
  const T = 'wahlwerk.vote.popular.tally';
</script>

<section>
  <h2>A vote</h2>
  <p>
    A vote turns many choices into one record. Each voter marks a Stimmzettel, the marks are
    counted per unit, and what is kept is a count, never a mark. wahlwerk reads the record and
    never models how a voter decides. For a popular vote the record is a <b>tally</b>, and the
    tally is the input of every allocation.
  </p>
  {#if sketches}
    <Plate plate={sketches.plates.vote}>
      The counts are those of one Wahlbezirk, <code>{sketches.unit}</code>, in the
      <a href="#data-{sketches.key}">Landtagswahl Sachsen-Anhalt 2026</a>, read through the engine;
      the drawing is schematic, the numbers are not.
    </Plate>
  {/if}
  <CodeRef
    names={[
      'wahlwerk.vote.popular.popular_vote.PopularVote',
      `${T}.Tally`,
      `${T}.TallyRow`,
      'wahlwerk.io.bundle.read_bundle',
    ]}
  />
</section>

<section>
  <h2>Who votes</h2>
  <p>
    Two kinds of voter, told apart less by how many they are than by whether the voter is
    known.
  </p>
  <ul>
    <li>
      <b>The electorate</b> casts a <b>popular vote</b>: thousands to millions of
      Wahlberechtigte, voting in secret (<Law id="de.bund.gg">Art. 38 (1) GG</Law>), each in one
      Wahlbezirk of one Wahlkreis. No choice is recorded, only counts per unit, and the counts are
      summed up the electoral hierarchy. What is decided is decided on the sums: a Wahlkreis
      winner from the Wahlkreis's Erststimmen, the seats from the Land's Zweitstimmen.
    </li>
    <li>
      <b>The members of a body</b> cast a <b>chamber vote</b>: a handful to several hundred
      people, each holding a mandate. Every mandate has one choice, yes, no, abstain or none, and
      the result is reckoned against the members, not the voters: the Bundeskanzler needs a
      majority of the Bundestag's members (<Law id="de.bund.gg">Art. 63 (2) GG</Law>). A
      namentliche Abstimmung records each member's choice
      (<Law id="de.bund.gobt">Sec. 52 GO-BT</Law>); a secret vote records only the counts.
    </li>
  </ul>
  {#if sketches}<Plate plate={sketches.plates.who} />{/if}
  <p class="note">
    A <b>chamber</b> means what it means in the engine: the mandates that constitute a body at
    one time, so a committee, a Gemeinderat and the Bundesversammlung each have one. The
    Bundesrat will test the word: a Land casts its votes only en bloc
    (<Law id="de.bund.gg">Art. 51 (3) GG</Law>), so there a mandate carries a weight. Chamber
    votes are not modelled yet; <code>vote/chamber/</code> is empty.
  </p>
  <h3>One model or two?</h3>
  <p>
    Open. What the two kinds share is what is voted on: sections, options, marks. What they do
    not share is the record. A tally has no identities and is summed along units; a chamber vote
    has one choice per mandate and is reckoned against the chamber that cast it. The engine keeps
    them apart for now, the popular vote in <code>vote/popular/</code> and the chamber vote in
    <code>vote/chamber/</code>, and will share what is the same once the second is written.
  </p>
  <CodeRef names={['wahlwerk.state.chamber.Chamber', 'wahlwerk.state.mandate.Mandate']} />
</section>

<section>
  <h2>What is voted on</h2>
  <p>
    A Stimmzettel has one or more <b>sections</b>, each a question of its own and counted apart:
    the Erststimme and the Zweitstimme of a Landtagswahl are two sections of one vote. Two votes on
    one day, a Landtagswahl and a Volksentscheid, are two votes. Within a section the voter
    chooses among <b>options</b>:
  </p>
  {#if sketches}<Plate plate={sketches.plates.what} />{/if}
  <p>
    The first four are counts per option, which is what a tally holds: a person is a candidate's
    row, an option a row for yes or no, Kumulieren a bigger count and Panaschieren more rows. A
    ranking is not. It needs one count for every distinct order, a ballot profile, which the
    tally does not hold. German public elections do not rank; the Irish Dáil, elected by single
    transferable vote, does.
  </p>
  <CodeRef names={[`${T}.TallyRow`]} />
</section>

<section>
  <h2>What is recorded</h2>
  <p>Per unit, a tally records four kinds of count:</p>
  <ul>
    <li>
      <code>eligible</code>: the Wahlberechtigte of a Wahlbezirk. A Briefwahlbezirk has none;
      nobody is registered there.
    </li>
    <li><code>voters</code>: the Wähler who cast a Stimmzettel, which is the turnout.</li>
    <li><code>invalid</code>: the ungültige Stimmen, per section.</li>
    <li><code>votes</code>: the valid votes for one party, candidate or option, per section.</li>
  </ul>
  <p>
    Each count names its section, its channel (<code>urne</code> or <code>brief</code>) and what
    it is for. Valid totals, the Gültige, are not stored: they are the sum of the
    <code>votes</code> rows, and a law that needs them sums. A blank field is absent, never zero:
    a party that did not stand has no row, one that stood and got nothing has a row with 0.
  </p>
  {#if sketches}<Plate plate={sketches.plates.recorded} />{/if}
  <CodeRef
    names={[
      `${T}.TallyKind`,
      `${T}.TallyRow`,
      `${T}.Level`,
      'wahlwerk.vote.popular.hierarchy.Hierarchy',
    ]}
  />
</section>

<Hierarchies />

<RefList {references} statutes={STATUTES} data={DATA} />
