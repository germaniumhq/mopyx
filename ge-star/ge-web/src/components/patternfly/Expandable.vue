<template>
<div :class="cssClasses">
  <button type="button"
          class="pf-c-expandable__toggle"
          :aria-expanded="expandedState"
          @click="onClick">
    <i class="fas fa-angle-right pf-c-expandable__toggle-icon" aria-hidden="true"></i>
    <span>{{label}}</span>
  </button>
  <div class="pf-c-expandable__content" v-if="expandedState"><slot>slot-default</slot></div>
</div>    
</template>

<script lang="ts">
import { Vue, Component, Prop, Provide } from 'vue-property-decorator'
import { request } from 'http';

@Component({})
export default class Expandable extends Vue {
    @Prop() expanded! : boolean
    @Prop() label! : string

    expandedState: boolean = false

    beforeMount() {
        this.expandedState = this.expanded
    }

    onClick() {
        this.expandedState = ! this.expandedState

        if (this.expandedState) {
            this.$emit("expand")
        } else {
            this.$emit("collapse")
        }
    }

    get cssClasses() {
        return {
            "pf-c-expandable": true,
            "pf-m-expanded": this.expandedState,
        }
    }
}
</script>
