<template>
    <div>
      <AboutModalBox @close="onCloseAboutBox" v-if="aboutModalBox"/>
      <Page :show-left-navigation="model.ui.left_navigation">
        <template v-slot:brand>
          <ToggleNavigation @click="onToggleLeftNavigation">
            <img src="../../assets/logo-onlysvg.svg"
                  width="32"
                  height="32"/>
            ge*
          </ToggleNavigation>
        </template>

        <template v-slot:navigation>
          <TopNavigation>
            <TopNavigationLink caption="Projects" :active="model.ui.section == 'overview'" route="/"/>
            <TopNavigationLink caption="Data" :active="model.ui.section == 'data'" route="/data"/>
            <TopNavigationLink caption="Reports" :active="model.ui.section == 'reports'" route="/reports"/>

            <!-- projects -->
            <template v-slot:right-nav>
              <Dropdown label="<<select project>>">
                <DropdownEntry>AE</DropdownEntry>
                <DropdownEntry>Wolverine</DropdownEntry>
                <DropdownEntry>Wut</DropdownEntry>
              </Dropdown>
            </template>
          </TopNavigation>
        </template>

        <template v-slot:tools>
          <Gravatar email="bogdan.mustiata@gmail.com"/>
          <AppMenu>
            <AppMenuEntry @click="onShowAbout">About</AppMenuEntry>
          </AppMenu>
        </template>

        <template v-slot:left-navigation>
          <slot name="left-navigation">slot-left-navigation</slot>
        </template>

        <section class="pf-c-page__main-section">
          <slot></slot>
        </section>
      </Page>
    </div>
</template>

<script lang="ts">
import AppMenu from '@/components/app/AppMenu.vue'
import AppMenuEntry from '@/components/app/AppMenuEntry.vue'
import Gravatar from '@/components/app/Gravatar.vue'
import ToggleNavigation from '@/components/app/ToggleNavigation.vue'
import TopNavigation from '@/components/patternfly/TopNavigation.vue'
import TopNavigationLink from '@/components/patternfly/TopNavigationLink.vue'
import TreeNodeView from '@/components/app/TreeNodeView.vue'

import hotkeys from 'hotkeys-js'

import AboutModalBox from '@/components/patternfly/AboutModalBox.vue'
import Page from '@/components/patternfly/Page.vue'
import Backdrop from '@/components/patternfly/Backdrop.vue'

import {Component, Vue} from 'vue-property-decorator'

import model from '@/model'
import Dropdown from "@/components/patternfly/Dropdown.vue";
import DropdownEntry from "@/components/patternfly/DropdownEntry.vue";

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
