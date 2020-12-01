<template>
  <div :class="cssClasses" :style="cssStyles" role="tooltip" v-if="visible">
    <div class="pf-c-tooltip__arrow"></div>
    <div class="pf-c-tooltip__content" id="tooltip-top-content"><slot></slot></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import {box} from "@/components/patternfly/domutil";

@Component({})
export default class Tooltip extends Vue {
  @Prop()
  'for'!: string;

  @Prop()
  position!: 'auto'|'top'|'left'|'right'|'bottom';

  renderPosition: 'auto'|'top'|'left'|'right'|'bottom' = 'auto'
  visible: boolean

  private mountedElements!: Array<Element> | NodeListOf<Element>;
  private currentTarget!: EventTarget | null;

  private tooltipWidth: int = 100
  private tooltipHeight: int = 48

  constructor() {
    super()

    // FIXME: seems lame
    if (this.position) {
      this.renderPosition = this.position;
    }

    this.visible = false
  }

  get cssClasses(): any {
    const result: {[name: string]: boolean} = {
      'pf-c-tooltip': true,
    }

    const renderPosition = this.renderPosition != "auto" ? this.renderPosition : "right"
    result[`pf-m-${renderPosition}`] = true

    return result
  }

  showTooltip(ev: Event) {
    this.currentTarget = ev.currentTarget
    this.visible = true;
  }

  hideTooltip() {
    this.currentTarget = null
    this.visible = false;
  }

  mounted(): void {
    this.mountedElements = this.findElements()

    this.mountedElements.forEach((target: Element) => {
      target.addEventListener("mouseenter", this.showTooltip)
      target.addEventListener("mouseleave", this.hideTooltip)
      target.addEventListener("focus", this.showTooltip)
      target.addEventListener("blur", this.hideTooltip)
    })
  }

  beforeUpdate() {
    if (this.$el.nodeType != 1) {
      return
    }

    const dimensions = box(this.$el)
    this.tooltipHeight = dimensions.height
    this.tooltipWidth = dimensions.width
  }

  get cssStyles() {
    if (!this.currentTarget) {
      return {}
    }

    const targetDimensions = box(this.currentTarget)

    switch (this.renderPosition) {
      case "bottom":
        return {
          left: `${targetDimensions.center - this.tooltipWidth / 2}px`,
          top: `${targetDimensions.bottom + 12}px`,
          position: "absolute",
        }
      case "top":
        return {
          left: `${targetDimensions.center - this.tooltipWidth / 2}px`,
          top: `${targetDimensions.top - this.tooltipHeight - 12}px`,
          position: "absolute",
        }
      case "left":
        return {
          left: `${targetDimensions.left - this.tooltipWidth - 12}px`,
          top: `${targetDimensions.middle - this.tooltipHeight / 2}px`,
          position: "absolute",
        }
      case "right":
      case "auto":
        return {
          left: `${targetDimensions.right + 12}px`,
          top: `${targetDimensions.middle - this.tooltipHeight / 2}px`,
          position: "absolute",
        }
    }

    throw new Error(`Unable to find positions for ${this.renderPosition}`)
  }

  beforeDestroy() {
    this.mountedElements.forEach((target: Element) => {
      target.removeEventListener("mouseenter", this.showTooltip)
      target.removeEventListener("mouseleave", this.hideTooltip)
      target.removeEventListener("focus", this.showTooltip)
      target.removeEventListener("blur", this.hideTooltip)
    })
  }

  findElements() {
    if (!this['for']) {
      return [this.$parent.$el]
    }

    return document.querySelectorAll(this['for'])
  }
}
</script>
