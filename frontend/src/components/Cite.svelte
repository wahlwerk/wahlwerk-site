<script lang="ts">
  // A citation in running text: the reference's number, linking to the list at the
  // foot of the page. Numbers come from the page's citer (lib/citations.ts).
  export let n: number;
  export let key: string;
</script>

<sup class="cite"><a href="#ref-{key}" aria-label="reference {n}">{n}</a></sup>

<style>
  .cite {
    font: 600 0.68em/0 var(--sans);
    margin-left: 1px;
  }
  .cite a {
    text-decoration: none;
    color: var(--accent);
  }
</style>
