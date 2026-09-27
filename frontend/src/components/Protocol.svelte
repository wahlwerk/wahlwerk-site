<script lang="ts">
  // The LWG LSA as the engine writes it (law/de/st/lwg.py, LWG_2021). The
  // step names and fields follow that file; keep them in step with it.
  interface Step {
    step: string;
    text: string;
    law: string;
  }

  const before: Step[] = [
    { step: 'SumVotes(level="wahlkreis")', text: 'count per Wahlbezirk and Briefwahlbezirk, sum to the Wahlkreis', law: '§§ 31, 32' },
    { step: 'ElectDistricts(section="erststimme", level="wahlkreis")', text: 'most Erststimmen wins; equal votes are a Tie, decided by lot', law: '§ 33' },
    { step: 'SumVotes(level="land")', text: 'Zweitstimmen per Landeswahlvorschlag', law: '§ 35 (2)' },
    { step: 'ApplyThreshold(threshold=RelativeThreshold(share=5/100), section="zweitstimme", level="land")', text: '5 % of valid Zweitstimmen; no Grundmandatsklausel', law: '§ 35 (3)' },
    { step: 'SetHouse(seats=83)', text: 'the legal size of the Landtag', law: '§ 1 (1)' },
  ];

  const allocateHouse: Step[] = [
    { step: 'SetSeatTotal()', text: 'the house less the Wahlkreise won by Einzelbewerber and by parties under 5 %', law: '§ 35 (4)' },
    { step: 'ApportionSeats(method=MajorityFirst(method=HareNiemeyer()))', text: 'Hare-Niemeyer; more than half the votes but not more than half the seats: one remainder seat first', law: '§ 35 (5), (6)' },
    { step: 'DeductDistrictSeats()', text: 'entitlement less Wahlkreis seats gives list seats and Mehrsitze', law: '§ 35 (7)' },
  ];

  const after: Step[] = [
    { step: 'FormChamber(minimum_mandates=83)', text: 'a mandate per seat: wk.001 …, then list.afd.001 …', law: '§ 1 (1)' },
  ];
</script>

<section>
  <h2>An electoral law as a protocol</h2>
  <p>
    A law is not six fixed slots but an ordered tuple of steps over one working record, the
    <code>Allocation</code>. Each step declares the facts it reads and writes, so a law written in
    the wrong order fails before it runs. A step may hold a protocol of its own, which is how the
    loop of § 35 (8) LWG LSA is written without special cases.
  </p>
  <ol class="protocol">
    {#each before as s}
      <li><span class="step">{s.step}<small>{s.text}</small></span><span class="law">{s.law}</span></li>
    {/each}
    {#each allocateHouse as s}
      <li><span class="step">{s.step}<small>{s.text}</small></span><span class="law">{s.law}</span></li>
    {/each}
    <li class="loop-wrap">
      <div class="loop">
        <div class="loop-head">
          <b>RepeatForMehrsitze(factor=2, full_rounds=2, fraktion=FraktionSize(...))</b>
          <span class="law">§ 35 (8), (8a)</span>
        </div>
        <p class="loop-text">
          While a party holds more Wahlkreis seats than it is entitled to: add twice their number
          and run the three steps above again, twice; after that, only while the remaining
          Mehrsitze exceed half the Fraktion size.
        </p>
        <ol class="inner">
          {#each allocateHouse as s}
            <li><span class="step">{s.step}</span><span class="law">{s.law}</span></li>
          {/each}
        </ol>
      </div>
    </li>
    {#each after as s}
      <li><span class="step">{s.step}<small>{s.text}</small></span><span class="law">{s.law}</span></li>
    {/each}
  </ol>
  <p>
    A counterfactual is one field: <code>ApportionSeats(method=SainteLague())</code>. The
    <code>Allocation</code> after each step is the record of how the result was derived.
  </p>
</section>

<style>
  .protocol {
    list-style: none;
    padding: 0;
    counter-reset: step;
    max-width: none;
  }
  .protocol li {
    counter-increment: step;
    display: grid;
    grid-template-columns: 2.2em minmax(0, 1fr) auto;
    gap: 10px;
    align-items: baseline;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 9px 12px;
  }
  .protocol li::before {
    content: counter(step);
    font: 500 0.8rem var(--mono);
    color: var(--muted);
  }
  .step {
    font-family: var(--mono);
    font-size: 0.88rem;
    overflow-wrap: anywhere;
  }
  .step small {
    display: block;
    font-family: var(--sans);
    font-size: 0.8rem;
    color: var(--muted);
  }
  .protocol li.loop-wrap {
    display: block;
    background: none;
    border: none;
    padding: 0;
  }
  .protocol li.loop-wrap::before {
    content: none;
  }
  .loop {
    border: 1.5px dashed var(--accent);
    border-radius: 8px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .loop-head {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    font-size: 0.85rem;
  }
  .loop-head b {
    font-family: var(--mono);
    font-weight: 500;
    overflow-wrap: anywhere;
  }
  .loop-text {
    font-size: 0.84rem;
    color: var(--muted);
  }
  .inner {
    list-style: none;
    padding: 0;
    max-width: none;
  }
  .protocol .inner li {
    counter-increment: none;
  }
  .protocol .inner li::before {
    content: '↻';
  }
</style>
