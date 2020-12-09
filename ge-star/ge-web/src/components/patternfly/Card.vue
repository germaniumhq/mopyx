<template>
  <div class="pf-c-card">
    <div class="pf-c-card__header" v-if="$slots.actions || $slots.title">
      <div class="pf-c-card__actions" v-if="$slots.actions">
        <slot name="actions"></slot>
      </div>
      <div class="pf-c-card__title" v-if="$slots.title">
        <slot name="title"></slot>
      </div>
    </div>
    <div class="pf-c-card__body"><slot></slot></div>
    <div class="pf-c-card__footer" v-if="$slots.footer"><slot name="footer"></slot></div>
  </div>
</template>

<script lang="ts">
import { Prop, Vue, Component } from 'vue-property-decorator'

@Component({})
export default class Card extends Vue {
}
</script>
