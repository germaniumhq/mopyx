<template>
  <li class="pf-c-nav__item">
    <slot></slot>
  </li>
</template>

<script lang="ts">
import { Prop, Vue, Component } from 'vue-property-decorator'

@Component({})
export default class JUnitCollector extends Vue {
}
</script>
