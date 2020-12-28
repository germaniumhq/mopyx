<template>
<Drop>
  <div :class="cssClasses">
    <button :class="cssScrollLeftButton"
            @click="onScrollLeft"
            aria-label="Scroll left">
      <i class="fas fa-angle-left" aria-hidden="true"></i>
    </button>
    <ul class="pf-c-tabs__list"
        ref="tabList"
        @scroll="onScrollTabs">
      <slot name="tabs"></slot>
    </ul>
    <button :class="cssScrollRightButton"
            @click="onScrollRight"
            aria-label="Scroll right">
      <i class="fas fa-angle-right" aria-hidden="true"></i>
    </button>
  </div>
  <div class="pf-m-fill">
    <slot></slot>
  </div>
</Drop>
</template>


<script lang="ts">
import {Component, Prop, Vue, Watch} from 'vue-property-decorator'
import { Drop } from 'vue-drag-drop'

@Component({
  components: {
    Drop,
  }
})
export default class Tabs extends Vue {
  tabsScrollLeft: number = 0
  tabsClientWidth: number = 0
  tabsScrollWidth: number = 0

  @Prop({default: false})
  secondary!: boolean

  onScrollTabs() {
    this.recomputeScrollProperties()
  }

  // we copy the properties on mount, and we update them on events
  // we only use computed properties in the CSS classes.
  mounted() {
    this.recomputeScrollProperties()
  }

  recomputeScrollProperties() {
    const tabList: Element = this.$refs.tabList as Element

    this.tabsScrollLeft = tabList.scrollLeft
    this.tabsClientWidth = tabList.clientWidth
    this.tabsScrollWidth = tabList.scrollWidth
  }

  get cssClasses() {
    // pf-c-tabs pf-m-start pf-m-start-current pf-m-end pf-m-tabs-secondary
    const result: Array<string> = [
        "pf-c-tabs",
        "pf-m-scrollable",
    ]

    if (this.secondary) {
      result.push("pf-m-secondary")
    } else {
      result.push("pf-m-box")
    }

    return result
  }

  get cssScrollLeftButton() {
    const result: {[name: string] : boolean} = {
        "pf-c-tabs__scroll-button": true,
        "hidden": true,
    }

    result["hidden"] = this.tabsScrollLeft == 0

    return result
  }

  get cssScrollRightButton() {
    const result: {[name: string] : boolean} = {
        "pf-c-tabs__scroll-button": true,
        "hidden": true,
    }

    if (this.tabsScrollLeft + this.tabsClientWidth < this.tabsScrollWidth) {
      result["hidden"] = false    
    }

    return result
  }

  onScrollLeft() {
    const tabList: Element = this.$refs.tabList as Element

    let scrollLeft

    if (tabList.scrollLeft > 40) {
      scrollLeft = tabList.scrollLeft - 40
    } else {
      scrollLeft = 0
    }

    tabList.scrollLeft = scrollLeft
    this.tabsScrollLeft = tabList.scrollLeft
  }

  onScrollRight() {
    const tabList: Element = this.$refs.tabList as Element

    let scrollLeft = tabList.scrollLeft + 40

    tabList.scrollLeft = scrollLeft
    this.tabsScrollLeft = tabList.scrollLeft
  }
}
</script>


<style type="scss">
.pf-m-secondary {
  background-color: white;
}

.hidden {
  display: none !important;
}
</style>
