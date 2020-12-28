<template>
  <router-link :to="route">
    <div :class="cssClasses">
      <img :src="logo"
           width="32"
           height="32"
           :alt="caption">
      <span>{{caption}}</span>
    </div>
  </router-link>
</template>

<script lang="ts">
import { Prop, Vue, Component } from 'vue-property-decorator'

@Component({})
export default class TopLogoLink extends Vue {
  @Prop() logo!: String
  @Prop() caption!: String
  @Prop() active!: Boolean
  @Prop() route!: String

  get cssClasses() {
    return {
      "pf-m-current": this.active,
      "logo-overview-link": true,
    }
  }
}
</script>

<style lang="scss">

.logo-overview-link {
  display: inline-block;
  vertical-align: middle;
  font-weight: normal;
  color: #ffffff;

  & span {
    vertical-align: middle;
  }

  & img {
    vertical-align: middle;
  }

  &.pf-m-current {
    color: var(--pf-c-nav__horizontal-list-link--hover--Color);
  }
}

</style>