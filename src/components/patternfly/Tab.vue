<template>
    <div :class="cssClasses" @click="onclick">
      <Drag :transfer-data="{}">
        <button class="pf-c-tabs__button"><Icon icon="far fa-file" class="tab-icon"/><slot></slot></button>
        <DragContainer slot="image" :model="this"/>
      </Drag>
    </div>
</template>

<style scoped>
i.tab-icon {
    margin-left: 1em;
    text-shadow: 1px 1px 2px #eeeeee;
    font-size: 0.75em;
}

.pf-c-tabs__button::before {
    border-bottom: none;    
}

.pf-c-tabs__item .pf-c-tabs__button {
  padding: 8px 20px 8px 8px;
}
</style>


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
    @Prop() icon!: string
    @Prop() label!: string

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
