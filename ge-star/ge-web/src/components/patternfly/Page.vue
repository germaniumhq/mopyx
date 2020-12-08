<template>
  <div class="pf-c-page">
<!--    <a class="pf-c-skip-to-content pf-c-button pf-m-primary" href="#main-content-page-layout-horizontal-nav">Skip to content</a>-->
    <header role="banner" class="pf-c-page__header">
      <div class="pf-c-page__header-brand">
        <slot name="brand">
          <a class="pf-c-page__header-brand-link">slot-brand</a>
        </slot>
      </div>

      <div class="pf-c-page__header-nav">
        <slot name="navigation">slot-navigation</slot>
      </div>

      <div class="pf-c-page__header-tools">
        <slot name="tools">slot-tools</slot>
      </div>
    </header>

    <div class="pf-c-page__sidebar"
         :hidden="!showLeftNavigation"
         v-if="$slots['left-navigation']">
      <div class="pf-c-page__sidebar-body">
        <slot name="left-navigation">slot-left-navigation</slot>
      </div>
    </div>

    <main role="main" class="pf-c-page__main" tabindex="-1">
      <slot></slot>
    </main>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'

@Component({})
export default class Page extends Vue {
    @Prop() showLeftNavigation!: boolean
}
</script>

<style scoped>
main {
  position: relative;
  overflow: hidden;
}

.pf-c-page {
  bottom: 0;
  right: 0;
  left: 0;
  top: 0;
  position: absolute;
}
</style>
