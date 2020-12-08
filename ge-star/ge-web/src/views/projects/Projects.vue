<template>
    <MainPage>
        <template slot="left-navigation">
            <TreeNodeView :model="model.projects.ge.files"/>
        </template>

        <GeDocumentEditor :editor="editors[0]"/>
    </MainPage>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

import MainPage from '@/components/app/MainPage.vue'
import TreeNodeView from '@/components/app/TreeNodeView.vue'

import model from '@/model'
import GeDocumentEditor from "@/components/app/GeDocumentEditor.vue";

@Component({
    components: {
        GeDocumentEditor,
        MainPage,
        TreeNodeView,
    }
})
export default class Projects extends Vue {
    model: any = model

    editors = model.open_editors
}
</script>
