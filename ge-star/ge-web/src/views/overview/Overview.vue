<template>
    <MainPage>
        <template slot="left-navigation">
            <TreeNodeView :model="model.projects.ge.files"/>
        </template>

      <Vega></Vega>
        <Card>
        </Card>
    </MainPage>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator'

import MainPage from '@/components/app/MainPage.vue'
import TreeNodeView from '@/components/app/TreeNodeView.vue'

import model from '@/model'
import GeDocumentEditor from "@/components/app/GeDocumentEditor.vue";
import Vega from "@/components/vega/Vega.vue";
import Card from "@/components/patternfly/Card.vue";
import Dropdown from "@/components/patternfly/Dropdown.vue";
import DropdownEntry from "@/components/patternfly/DropdownEntry.vue";

@Component({
    components: {
      DropdownEntry,
      Dropdown,
      Vega,
      Card,
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
