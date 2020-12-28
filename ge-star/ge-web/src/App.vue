<template>
  <div class="full-page">
    <Backdrop v-if="model.ui.backdrop"/>

    <router-view/>
  </div>
</template>

<style scoped>
</style>


<script lang="ts">

import hotkeys from 'hotkeys-js'
import Backdrop from '@germanium-vue-patternfly/Backdrop.vue'

import { Vue, Component } from 'vue-property-decorator'
import model from '@/model'

import '@/model/init'

@Component({
  components: {
    Backdrop,
  }
})
export default class App extends Vue {
  beforeMount() {
    hotkeys('alt+1', this.onToggleLeftNavigation)
  }

  data() {
    return {
      model,
    }
  }

  onToggleLeftNavigation() {
    model.ui.left_navigation = ! model.ui.left_navigation;
  }
}
</script>


<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>

