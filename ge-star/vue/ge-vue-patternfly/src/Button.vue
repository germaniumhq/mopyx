<template>
  <button :class="cssClasses" type="button"><slot>label</slot></button>    
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component({})
export default class Button extends Vue {
  @Prop({default: "primary"})
  type! : string

  get cssClasses() {
    const result: {[name: string] : boolean} = {
        "pf-c-button" : true,
    };

    result[`pf-m-${this.type}`] = true

    return result
  }
}
</script>
