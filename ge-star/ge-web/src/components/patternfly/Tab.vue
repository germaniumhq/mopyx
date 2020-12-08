<template>
  <li :class="cssClasses" @click="onclick">
    <Drag :transfer-data="{}">
      <button class="pf-c-tabs__link"><slot></slot></button>
      <DragContainer slot="image" :model="this"/>
    </Drag>
  </li>
</template>

<script lang="ts">
import { Drag } from 'vue-drag-drop'
import { Component, Prop, Vue } from 'vue-property-decorator'

import Icon from '@/components/app/Icon.vue'
import DragContainer from '@/components/app/DragContainer.vue'

@Component({
    components: {
        Drag,
        DragContainer,
        Icon,
    }
})
export default class Tab extends Vue {
    @Prop() active!: boolean
    @Prop({default: ""}) icon!: string

    get cssClasses() {
        const result: {[name: string] : boolean} = {
            "pf-c-tabs__item": true,
        }

        if (this.active) {
            result["pf-m-current"] = true
        }

        return result
    }

    onclick(ev: MouseEvent) {
        this.$emit("click", ev)
    }
}
</script>
