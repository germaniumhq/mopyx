<template>
    <MainPage>
        <template slot="left_navigation">
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
import Flex from "@/components/patternfly/Flex.vue";
import FlexItem from "@/components/patternfly/FlexItem.vue";

@Component({
    components: {
      FlexItem,
      Flex,
        GeDocumentEditor,
        MainPage,
        TreeNodeView,
    }
})
export default class Tests extends Vue {
    model: any = model

    editors = model.open_editors
}
</script>
