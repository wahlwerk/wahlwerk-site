<script lang="ts">
  // The four roles: the vote is input, the law a protocol, allocating seats
  // a process, and the chamber new state.
  const nodes = [
    { role: 'input', name: 'PopularVote', text: 'the Tally and its Source; holds no law' },
    { role: 'protocol', name: 'Law.protocol', text: 'the electoral law: an ordered tuple of steps' },
    { role: 'process', name: 'allocate(vote, protocol)', text: 'applies each step to an Allocation' },
    { role: 'state', name: 'Chamber', text: 'mandates wk.001 …, list.afd.001 …' },
  ];

  const pieces = [
    ['PopularVote', 'vote/popular/', 'what the electorate recorded: the tally and its source'],
    ['Tally', 'vote/popular/', 'the long table of rows: filter, sum_to, sum_by, total; never stores a sum'],
    ['Level, Hierarchy', 'vote/popular/', 'the main (electoral) hierarchy in the ids, and alternative ones beside it'],
    ['apportionment methods', 'apportionment/', 'Hare-Niemeyer, d’Hondt, Sainte-Laguë; any keys, exact weights, no German content; seats or a Tie'],
    ['thresholds, Ausgleich', 'apportionment/', 'relative and seat thresholds, exemptions, “or” over them; Überhang and Ausgleich; majority clauses'],
    ['Law', 'law/', 'one law version as one object with its protocol; a registry finds the law in force for a body and date'],
    ['Allocation, AllocationStep', 'process/allocation/', 'the working record, and the rules that fill it; each step declares what it reads and writes'],
    ['Chamber, Mandate, Caucus', 'state/', 'the chamber a process forms: seats, and the caucuses over them'],
    ['measures', 'measure/', 'Loosemore-Hanby, Gallagher, Sainte-Laguë and d’Hondt indices, and more; exact'],
  ];
</script>

<section>
  <h2>The pieces</h2>
  <p>
    The vote is input, the law is a protocol, allocating seats is a process, and the chamber is
    new state. A counterfactual is the same vote under a different protocol.
  </p>
  <div class="flow" role="list">
    {#each nodes as node}
      <div class="node" class:proc={node.role === 'process'} role="listitem">
        <span class="role">{node.role}</span>
        <b>{node.name}</b>
        <span>{node.text}</span>
      </div>
    {/each}
  </div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Piece</th><th>Where</th><th>What it is</th></tr></thead>
      <tbody>
        {#each pieces as [name, where, what]}
          <tr><td><code>{name}</code></td><td><code>{where}</code></td><td>{what}</td></tr>
        {/each}
      </tbody>
    </table>
  </div>
</section>

<section>
  <h2>Why the vote does not build its chamber</h2>
  <p>
    Votes are input. If <code>PopularVote</code> formed the chamber, it would have to own the law,
    and replaying the same votes under another law would need a second vote object. Forming a
    chamber creates a new unit, so it is an external process: the function
    <code>allocate</code>, not a method on the vote or the chamber.
  </p>
</section>

<style>
  .flow {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
  }
  @media (max-width: 640px) {
    .flow { grid-template-columns: 1fr 1fr; }
  }
  .node {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .node.proc {
    border: 1.5px solid var(--accent);
  }
  .node b {
    font-family: var(--mono);
    font-weight: 500;
    font-size: 0.9rem;
    overflow-wrap: anywhere;
  }
  .node span {
    font-size: 0.82rem;
    color: var(--muted);
    line-height: 1.4;
  }
  .node .role {
    font: 600 0.68rem/1 var(--sans);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent);
  }
</style>
