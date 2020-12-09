<template>
  <div class="pf-l-flex__item">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { Prop, Vue, Component } from 'vue-property-decorator'

@Component({})
export default class FlexItem extends Vue {
}
</script>
