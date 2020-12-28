<template>
  <img class="pf-c-avatar"
       :src="src"
       :alt="alt" />
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: {
    alt: String,
    src: String,    
  }
})
</script>
