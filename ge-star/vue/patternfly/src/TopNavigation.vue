<template>
  <nav class="pf-c-nav pf-m-horizontal" aria-label="Global">
<!--    <button class="pf-c-nav__scroll-button" disabled aria-label="Scroll left">-->
<!--      <i class="fas fa-angle-left" aria-hidden="true"></i>-->
<!--    </button>-->
    <ul class="pf-c-nav__list">
      <slot></slot>
    </ul>
<!--    <button class="pf-c-nav__scroll-button" disabled aria-label="Scroll right">-->
<!--      <i class="fas fa-angle-right" aria-hidden="true"></i>-->
<!--    </button>-->
  </nav>

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
