<template>
  <div class="pf-l-flex">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { Prop, Vue, Component } from 'vue-property-decorator'

@Component({})
export default class Flex extends Vue {
}
</script>
