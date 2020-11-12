<template>
  <div class="pf-c-tooltip pf-m-top" role="tooltip">
    <div class="pf-c-tooltip__arrow"></div>
    <div class="pf-c-tooltip__content" id="tooltip-top-content"><slot></slot></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'

@Component({})
export default class Tooltip extends Vue {
}
</script>
