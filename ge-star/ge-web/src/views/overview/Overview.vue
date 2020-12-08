<template>
    <MainPage>
        <template slot="left-navigation">
            <TreeNodeView :model="model.projects.ge.files"/>
        </template>

        <Vega></Vega>
    </MainPage>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

import MainPage from '@/components/app/MainPage.vue'
import TreeNodeView from '@/components/app/TreeNodeView.vue'

import model from '@/model'
import GeDocumentEditor from "@/components/app/GeDocumentEditor.vue";
import Vega from "@/components/vega/Vega.vue";

@Component({
    components: {
      Vega,
        GeDocumentEditor,
        MainPage,
        TreeNodeView,
    }
})
export default class Overview extends Vue {
    model: any = model

    editors = model.open_editors
}
</script>
