<template>
  <li class="pf-c-nav__item">
    <router-link :to="route" :class="cssClasses" >
      {{caption}}
    </router-link>
  </li>
</template>

<script lang="ts">
import { Prop, Vue, Component } from 'vue-property-decorator'

@Component({})
export default class TopNavigationLink extends Vue {
  @Prop() caption!: String
  @Prop() active!: Boolean
  @Prop() route!: String

  get cssClasses() {
    return {
      "pf-c-nav__link": true,
      "pf-m-current": this.active,
    }
  }
}
</script>
