<template>
  <DropdownEntry :disabled="disabled"
                  @click="onClick"><slot></slot></DropdownEntry>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit } from 'vue-property-decorator'
import DropdownEntry from '@/components/patternfly/DropdownEntry.vue'

@Component({
    components: {
        DropdownEntry
    }
})
export default class AppMenuEntry extends Vue {
    @Prop({default: false}) disabled! : boolean

    @Emit("click")
    onClick() {
    }
}
</script>
