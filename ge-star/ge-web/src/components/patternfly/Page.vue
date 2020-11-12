<template>
     <div class="pf-c-page">
    <header role="banner" class="pf-c-page__header">
      <div class="pf-c-page__header-brand">
        <slot name="brand">
          <a class="pf-c-page__header-brand-link">slot-brand</a>
        </slot>
      </div>

      <slot name="navigation">slot-navigation</slot>

      <div class="pf-c-page__header-tools">
        <slot name="tools">slot-tools</slot>
      </div>
    </header>
    <div class="pf-c-page__sidebar pf-m-dark" :hidden="!showLeftNavigation">
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
