<template>
 <div class="pf-c-page__header-nav">
  <slot name="left-nav"></slot>
  <nav class="pf-c-nav" aria-label="Global">
    <button class="pf-c-nav__scroll-button" aria-label="Scroll left">
      <i class="fas fa-angle-left" aria-hidden="true"></i>
    </button>
    <ul class="pf-c-nav__horizontal-list">
      <slot></slot>
    </ul>
    <button class="pf-c-nav__scroll-button" aria-label="Scroll right">
    <i class="fas fa-angle-right" aria-hidden="true"></i>
    </button>
  </nav>
  <slot name="right-nav"></slot>
 </div>
</template>

<style scoped>
</style>

<script lang="ts">

import { Vue, Component } from 'vue-property-decorator'

@Component({
})
export default class TopNavigation extends Vue {
}
</script>
