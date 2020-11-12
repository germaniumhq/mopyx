<template>
    <MainPage>
        <template slot="left-navigation">
            <TreeNodeView :model="model.projects.ge.files"/>
        </template>

        <CodeEditor :editor="editors[0]"/>
    </MainPage>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

import CodeEditor from '@/components/app/CodeEditor.vue'
import MainPage from '@/components/app/MainPage.vue'
import TreeNodeView from '@/components/app/TreeNodeView.vue'

import model from '@/model'

@Component({
    components: {
        CodeEditor,
        MainPage,
        TreeNodeView,
    }
})
export default class Overview extends Vue {
    model: any = model

    editors = model.open_editors
}
</script>
