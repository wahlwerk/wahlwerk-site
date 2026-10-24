<script lang="ts">
  // A statute cited inline, in its German form with the section (Art. 63 GG,
  // Sec. 35 (8) LWG LSA), linked to the version in the page's list of sources.
  /** The law id of the version cited, e.g. de.st.lwg.2021. */
  export let id: string;
</script>

<a class="law" href="#law-{id}"><slot /></a>

<style>
  a {
    white-space: nowrap;
  }
</style>
