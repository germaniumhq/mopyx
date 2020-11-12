<template>
<div class="pf-c-empty-state pf-m-lg">
  <slot name="icon"><i class="fas fa-cubes pf-c-empty-state__icon" aria-hidden="true"></i></slot>
  <h1 class="pf-c-title pf-m-lg"><slot name="title">slot-title</slot></h1>
  <div class="pf-c-empty-state__body">
      <slot>default-slot text</slot>
  </div>
  <slot name="primary">slot-primary <button class="pf-c-button pf-m-primary" type="button">Primary action</button></slot>
  <div class="pf-c-empty-state__secondary">
      <slot name="secondary">slot-secondary</slot>
  </div>
</div>
</template>


<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

@Component({
})
export default class EmptyState extends Vue {
}
</script>
