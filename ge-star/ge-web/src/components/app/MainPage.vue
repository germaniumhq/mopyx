<template>
    <div>
      <AboutModalBox @close="onCloseAboutBox" v-if="aboutModalBox"/>
      <Page :show-left-navigation="model.ui.left_navigation">
        <template v-slot:brand>
          <ToggleNavigation @click="onToggleLeftNavigation"/>
          <TopLogoLink route="/"
                       caption="ge*"
                       :logo="require('../../assets/logo-onlysvg.svg')"
                       :active="model.ui.section == 'overview'" />
        </template>

        <template v-slot:navigation>
          <TopNavigation>
            <TopNavigationLink caption="Tests" :active="model.ui.section == 'tests'" route="/tests"/>
<!--            <TopNavigationLink caption="Data" :active="model.ui.section == 'data'" route="/data"/>-->
            <TopNavigationLink caption="Reports" :active="model.ui.section == 'reports'" route="/reports"/>
          </TopNavigation>
        </template>

        <template v-slot:tools>
          <Dropdown label="<<select project>>">
            <DropdownEntry>AE</DropdownEntry>
            <DropdownEntry>Wolverine</DropdownEntry>
            <DropdownEntry>Wut</DropdownEntry>
          </Dropdown>
          <Gravatar email="bogdan.mustiata@gmail.com"/>
          <AppMenu>
            <AppMenuEntry @click="onShowAbout">About</AppMenuEntry>
          </AppMenu>
        </template>

        <template v-slot:left_navigation v-if="$slots.left_navigation">
          <slot name="left_navigation"></slot>
        </template>

        <section class="pf-c-page__main-section">
          <slot></slot>
        </section>
      </Page>
    </div>
</template>

<script lang="ts">
import Dropdown from "@germanium-vue-patternfly/Dropdown.vue";
import DropdownEntry from "@germanium-vue-patternfly/DropdownEntry.vue";
import TopLogoLink from "@germanium-vue-patternfly/TopLogoLink.vue";
import TopNavigation from '@germanium-vue-patternfly/TopNavigation.vue'
import TopNavigationLink from '@germanium-vue-patternfly/TopNavigationLink.vue'
import AboutModalBox from '@germanium-vue-patternfly/AboutModalBox.vue'
import Page from '@germanium-vue-patternfly/Page.vue'
import Backdrop from '@germanium-vue-patternfly/Backdrop.vue'

import AppMenu from '@/components/app/AppMenu.vue'
import AppMenuEntry from '@/components/app/AppMenuEntry.vue'
import Gravatar from '@/components/app/Gravatar.vue'
import ToggleNavigation from '@/components/app/ToggleNavigation.vue'
import TreeNodeView from '@/components/app/TreeNodeView.vue'

import hotkeys from 'hotkeys-js'

import {Component, Vue} from 'vue-property-decorator'

import model from '@/model'

@Component({
  components: {
    DropdownEntry,
    Dropdown,
    AboutModalBox,
    AppMenu,
    AppMenuEntry,
    Backdrop,
    Gravatar,
    Page,
    ToggleNavigation,
    TopLogoLink,
    TopNavigation,
    TopNavigationLink,
    TreeNodeView,
  }
})
export default class MainPage extends Vue {
  aboutModalBox: boolean = false

  beforeMount() {
    hotkeys('alt+1', this.onToggleLeftNavigation)
  }

  data() {
    return { 
      model,
    }
  }

  onShowAbout() {
    model.ui.backdrop = true
    this.aboutModalBox = true
  }

  onCloseAboutBox() {
    model.ui.backdrop = false
    this.aboutModalBox = false
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
</style>
