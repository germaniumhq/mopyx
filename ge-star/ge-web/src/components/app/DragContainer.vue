<template>
    <div class="drag-container">
        <Badge class="drag-badge">{{model.label}}</Badge>
    </div>    
</template>

<style scoped>
.drag-badge {
    text-shadow: -1px -1px 2px #000000;
    box-shadow: 1px 1px 4px #000000;
}

.drag-container {
    opacity: 1;
    padding: 4px;
}
</style>


<script lang="ts">
import Badge from '@/components/patternfly/Badge.vue'

import { Component, Vue, Prop } from 'vue-property-decorator';

@Component({
    components: {
        Badge,
    }
})
export default class DragContainer extends Vue {
    @Prop() model! : any
}
</script>

