<template>
<div :class='cssClasses'
     @blur="onBlur"
     @click="onClick">
  <button class="pf-c-dropdown__toggle pf-m-plain"
          id="dropdown-kebab-expanded-button" 
          :aria-expanded="expanded" 
          :aria-label="label">
    <i class="fas fa-ellipsis-v" aria-hidden="true"></i>
  </button>
  <ul v-if="expandedState"
      :class="dropdownCssClasses"
      aria-labelledby="dropdown-kebab-expanded-button">
    <slot></slot>
  </ul>
</div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit} from 'vue-property-decorator'

// FIXME: click outside doesn't closes the context menu
@Component({})
export default class Dropdown extends Vue {
  @Prop({default : false}) 
  expanded!: boolean

  @Prop({default: "Action"}) 
  label!: string

  @Prop({default: "left"})
  align!: string

  @Prop({default: "bottom"})
  valign!: string

  expandedState: boolean = true;

  beforeMount() {
    this.expandedState = this.expanded
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

  @Emit("click")
  onClick() {
    this.expandedState = !this.expandedState
  }

  @Emit("blur")
  onBlur() {
    this.expandedState = false
  }
}
</script>
