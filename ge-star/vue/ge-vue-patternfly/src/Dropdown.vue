<template>
<div :class='cssClasses'>
  <button class="pf-c-dropdown__toggle pf-m-plain"
          id="dropdown-kebab-expanded-button" 
          :aria-expanded="expanded" 
          :aria-label="label"
          @click="onClick">
    <span class="pf-c-dropdown__toggle-text" v-if="!ellipsis && label">{{label}}</span>
    <i class="fas fa-ellipsis-v" aria-hidden="true" v-if="ellipsis"></i>
    <span class="pf-c-dropdown__toggle-icon" v-else>
      <i class="fas fa-caret-down" aria-hidden="true"></i>
    </span>
  </button>
  <ul v-if="expandedState"
      :class="dropdownCssClasses"
      aria-labelledby="dropdown-kebab-expanded-button"
      ref="menu">
    <slot></slot>
  </ul>
</div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit} from 'vue-property-decorator'
import {isDomChild} from "./domutil";

@Component({})
export default class Dropdown extends Vue {
  $refs!: {
    menu: Element,
  }

  @Prop({default : false}) 
  expanded!: boolean

  @Prop({default : false})
  ellipsis!: boolean

  @Prop({default: ""})
  label!: string

  @Prop({default: "left"})
  align!: string

  @Prop({default: "bottom"})
  valign!: string

  expandedState: boolean = false;

  beforeMount() {
    this.expandedState = this.expanded
  }

  @Emit("click")
  onClick() {
    if (this.expandedState) {
      this.collapse()
      return
    }

    this.expand()
  }

  onBodyFocusEvent(e: FocusEvent) {
    if (!this.expandedState) {
      console.warn("Context menu not expanded")
      return
    }

    if (isDomChild(this.$refs.menu, e.target as Element)) {
      return;
    }

    this.collapse()
  }

  expand() {
    if (this.expandedState) {
      return
    }

    this.expandedState = true

    setTimeout(() => {
      document.body.addEventListener("focus", this.onBodyFocusEvent)
      document.body.addEventListener("click", this.collapse)
    }, 0)
  }

  collapse() {
    if (!this.expandedState) {
      return;
    }

    this.expandedState = false;
    document.body.removeEventListener("focus", this.onBodyFocusEvent)
    document.body.removeEventListener("click", this.collapse)
  }

  get cssClasses() {
    const result: {[name: string]: boolean} = {
      "pf-c-dropdown": true,
      "pf-m-expanded": this.expandedState,
    }

    if (this.valign == "top") {
      result["pf-m-top"] = true;
    }

    return result;
  }

  get dropdownCssClasses() {
    const result: {[name: string]: boolean} = {
      "pf-c-dropdown__menu": true,
    }

    if (this.align == "right") {
      result["pf-m-align-right"] = true;
    }

    return result;
  }
}
</script>
