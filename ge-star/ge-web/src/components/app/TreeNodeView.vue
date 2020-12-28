<template>
  <Drag :transfer-data="selection"
        @dragstart="onDragStart"
        @dragend="onDragEnd">
    <Drop @dragover="onDragEnter" @dragleave="onDragLeave">
        <div class="tree">
            <div :class="cssPlusClasses" 
                @click="onToggleExpand"><i class="fas fa-angle-right"></i></div>
            <div :class="cssIconLabelClasses" @click="onClickNode">
                <div class="tree-icon"><Icon :icon="cssIcon"/></div>
                <div class="tree-label">{{model.label}}</div>
            </div>
            <div class="tree-content" v-if="expandedState">
                <TreeNodeView :model="child"
                            v-for="child in model.children"
                            v-bind:key="child.label"/>
            </div>
        </div>
    </Drop>

    <DragContainer slot="image" :model="selection"/>
  </Drag>
</template>

<style scoped>
.tree {
    cursor: pointer;
}

.tree-plus-hidden, .tree-icon, .tree-plus {
    width: 16px;
    height: 16px;
    float: left;
    transition: all 0.1s ease-in;
}

.tree-plus-hidden {
    padding-left: 16px;
    overflow: hidden;
}

.tree-icon-label {
    border: solid 1px transparent;
    box-sizing: border-box;
    height: 22px;
}

.tree-label {
    margin-left: 40px;
    height: 20px;
    box-sizing: border-box;
}

.drag-over {
    border: blue dotted 1px
}

.selected {
    border: #ccccff33 solid 1px;
    background: #ccccff33;
}

.expanded {
    transform: rotate(90deg) translate(6px, 2px);
    transition: all 0.1s ease-in;
}

.tree-content {
    margin-left: 16px
}

</style>


<script lang="ts">
/* eslint no-console: ["off", { allow: ["warn", "error"] }] */

import DragContainer from '@germanium-vue-patternfly/DragContainer.vue'
import Icon from '@germanium-vue-patternfly/Icon.vue'

import { Component, Vue, Prop } from 'vue-property-decorator';
import { Drag, Drop } from 'vue-drag-drop';

import { TreeNode } from '@/model/ui'
import { selection } from '@/model/selection'

@Component({
    components: {
        DragContainer,
        Drag,
        Drop,
        Icon,
    }
})
export default class TreeNodeView extends Vue {
    @Prop() model!: TreeNode

    selection = selection

    expandedState: boolean = false

    dragOver: boolean = false

    get cssIconLabelClasses() {
        const result: {[name: string]: boolean} = {
            "tree-icon-label": true,
        };

        if (this.dragOver) {
            result["drag-over"] = true
        }

        if (selection.contains(this.model)) {
            result["selected"] = true
        }

        return result;
    }

    get cssIcon() {
        if (this.model.icon) {
            return this.model.icon;
        } else if (this.expandedState) {
            return "fa-folder-open";
        } else {
            return "fa-folder";
        }
    }

    get cssPlusClasses() {
        const result: {[name: string]: boolean} = {
        };

        if (!this.model.icon) {
            result['tree-plus'] = true
        } else {
            result['tree-plus-hidden'] = true            
        }

        if (this.expandedState) {
            result['expanded'] = true
        }

        return result;
    }

    onDragStart(data: any, ev: Event) {
        ev.stopPropagation()
    }

    onDragEnd() {
    }

    onDragEnter(data: any, ev: Event) {
        ev.stopPropagation()
        this.dragOver = true
    }

    onDragLeave() {
        this.dragOver = false
    }

    onToggleExpand() {
        this.expandedState = ! this.expandedState
    }

    onClickNode(ev: MouseEvent) {
        const isAlreadySelected = selection.contains(this.model)

        if (ev.ctrlKey && isAlreadySelected) {
            selection.delete(this.model)
        } else if (ev.ctrlKey && !isAlreadySelected) {
            selection.add(this.model)
        } else {
            selection.select(this.model)
        }
    } 
}
</script>
