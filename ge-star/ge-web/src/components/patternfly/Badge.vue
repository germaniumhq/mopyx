<template>
  <span :class="computedCssClasses"><slot></slot></span>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'

@Component({})
export default class Badge extends Vue {
    @Prop() read! : boolean

    get computedCssClasses() {
        const result: { [name: string] : boolean } = {
            "pf-c-badge": true
        }

        if (this.read) {
            result["pf-m-read"] = true
        } else {
            result["pf-m-unread"] = true
        }

        return result
    }
}
</script>
