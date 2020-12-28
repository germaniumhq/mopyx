<template>
  <div class="fill-parent">
    <Tabs v-if="editor.documents.length" class="fill-parent">
        <template v-slot:tabs>
            <Tab icon="fa-file"
                 @click="selectDocument(document.key)" 
                 :label="document.label"
                 v-for="document in editor.documents" 
                 :active='editor.activeDocument == document.key'
                 :key="document.key">{{document.label}}<Icon 
                        @click="closeDocument(document.key)"
                        icon="fa-times" 
                        class="close-icon"/></Tab>
        </template>

        <MonacoCodeEditor :document="document"
                          v-for="document in editor.documents"
                          :key="document.key"
                          :hidden="editor.activeDocument != document.key"/>
    </Tabs>
    
    <EmptyState v-else="">
      <template v-slot:title>
          No files open
      </template>

      Open or create a file

      <template v-slot:primary><div/></template>
      <template v-slot:secondary><div/></template>
    </EmptyState>
  </div>
</template>

<style scoped>

.fill-parent {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
}

.close-icon {
    color: #cccccc;
    visibility: hidden;
    text-shadow: 1px 1px 2px #eeeeee;
    font-size: 0.6em;
    position: absolute;
    z-index: 1;
    padding: 2px;
    right: 4px;
    top: 13px;
}

.pf-c-tabs__button:hover .close-icon {
    visibility: visible;
}

.pf-m-current .close-icon {
    visibility: visible;
}

.pf-m-current {
    background-color: white;
}
</style>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

import Tabs from '@germanium-vue-patternfly/Tabs.vue'
import Tab from '@germanium-vue-patternfly/Tab.vue'
import Icon from '@germanium-vue-patternfly/Icon.vue'

import MonacoCodeEditor from '@/components/app/MonacoCodeEditor.vue'

import EmptyState from '@germanium-vue-patternfly/EmptyState.vue'

import { CodeEditor as EditorModel, CodeDocument } from '@/model/ui'
import { unregisterDocument } from '@/model/actions/editor'
import { unregisterEditor } from '../../monaco_support'

@Component({
    components: {
        EmptyState,
        Icon,
        MonacoCodeEditor,
        Tab,
        Tabs,
    }
})
export default class CodeEditor extends Vue {
    @Prop() editor!: EditorModel

    selectDocument(documentKey: string): void {
        this.editor.activeDocument = documentKey
    }

    closeDocument(documentKey: string): void {
        unregisterDocument(this.editor, documentKey)
        unregisterEditor(documentKey)
    }

    get activeDocument(): CodeDocument | null {
        for (let i = 0; i < this.editor.documents.length; i++) {
            const document = this.editor.documents[i];
            if (document.key == this.editor.activeDocument) {
                return document
            }
        }
        
        return null
    }
}
</script>
