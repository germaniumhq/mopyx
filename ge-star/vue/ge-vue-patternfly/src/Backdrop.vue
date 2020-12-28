<template>
    <div class="pf-c-backdrop"></div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class Backdrop extends Vue {
  beforeMount() {
    document.body.classList.add("pf-c-backdrop__open")
  }

  beforeDestroy() {
    document.body.classList.remove("pf-c-backdrop__open")
  }
}
</script>
