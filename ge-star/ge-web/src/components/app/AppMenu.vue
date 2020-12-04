<template>
    <Dropdown align="right" :ellipsis="true"><slot></slot></Dropdown>
</template>

<script lang="ts">
import { Vue, Component, Prop} from 'vue-property-decorator'
import Dropdown from '@/components/patternfly/Dropdown.vue' 

@Component({
    components: {
        Dropdown,
    }
})
export default class AppMenu extends Vue {
}
</script>
