<template>
  <div class="pf-c-about-modal-box" role="dialog" aria-modal="true" aria-labelledby="about-modal-title"
    style="position: absolute; margin-left: auto; margin-right: auto">
    <div class="pf-c-about-modal-box__brand">
      <img class="pf-c-about-modal-box__brand-image" src="/assets/images/pf_mini_logo_white.svg" alt="PatternFly brand logo" />
    </div>
    <div class="pf-c-about-modal-box__close">
      <button class="pf-c-button pf-m-plain" type="button" aria-label="Close dialog" @click="onClose">
        <i class="fas fa-times" aria-hidden="true"></i>
      </button>
    </div>
    <div class="pf-c-about-modal-box__header">
      <h1 class="pf-c-title pf-m-4xl" id="about-modal-title">Germanium Star</h1>
    </div>
    <div class="pf-c-about-modal-box__hero"></div>
    <div class="pf-c-about-modal-box__content">
      <div class="pf-c-about-modal-box__body">content</div>
      <p class="pf-c-about-modal-box__strapline">Trademark and copyright information here</p>
    </div>
  </div>
</template>

<style scoped>
.pf-c-about-modal-box {
  margin: auto;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
}
</style>


<script lang="ts">
import { Component, Vue, Prop, Emit } from 'vue-property-decorator'

@Component({})
export default class AboutModalBox extends Vue {
  @Emit("close")
  onClose() {}
}
</script>
