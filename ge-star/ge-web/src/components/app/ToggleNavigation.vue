

<template>
  <div class="pf-c-page__header-brand-toggle toggle-navigation" @click="onClick">
    <i class="fas fa-bars"></i>
    <slot></slot>
  </div>
</template>

<style lang="scss" scoped>
.fas {
  margin-right: 1em;
}

.toggle-navigation {
  height: 48px;
  line-height: 48px;
  cursor: pointer;

  * {
      vertical-align: middle;
  }
}

</style>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

@Component({})
export default class ToggleNavigation extends Vue {
    onClick() {
        this.$emit("click")
    }
}
</script>
