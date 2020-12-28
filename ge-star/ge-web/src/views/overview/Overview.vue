<template>
    <MainPage>
      <Flex>
        <FlexItem>
        <Card>
          <template v-slot:title>Test Results</template>
          <template v-slot:actions>
            <Dropdown :ellipsis="true">
              <DropdownEntry>wut</DropdownEntry>
            </Dropdown>
          </template>
          <Vega></Vega>
        </Card>
        </FlexItem>

        <FlexItem>
        <Card>
          <template v-slot:title>Test Results</template>
          <template v-slot:actions>
            <Dropdown :ellipsis="true">
              <DropdownEntry>wut</DropdownEntry>
            </Dropdown>
          </template>
          <Vega></Vega>
        </Card>
        </FlexItem>

        <FlexItem>
          <Card>
            <template v-slot:title>Test Results</template>
            <template v-slot:actions>
              <Dropdown :ellipsis="true">
                <DropdownEntry>wut</DropdownEntry>
              </Dropdown>
            </template>
            <Vega></Vega>
          </Card>
        </FlexItem>

        <FlexItem>
          <Card>
            <template v-slot:title>Test Results</template>
            <template v-slot:actions>
              <Dropdown :ellipsis="true">
                <DropdownEntry>wut</DropdownEntry>
              </Dropdown>
            </template>
            <Vega></Vega>
          </Card>
        </FlexItem>

        <FlexItem>
          <Card>
            <template v-slot:title>Test Results</template>
            <template v-slot:actions>
              <Dropdown :ellipsis="true">
                <DropdownEntry>wut</DropdownEntry>
              </Dropdown>
            </template>
            <Vega></Vega>
          </Card>
        </FlexItem>

        <FlexItem>
          <Card>
            <template v-slot:title>Test Results</template>
            <template v-slot:actions>
              <Dropdown :ellipsis="true">
                <DropdownEntry>wut</DropdownEntry>
              </Dropdown>
            </template>
            <Vega></Vega>
          </Card>
        </FlexItem>

        <FlexItem>
          <Card>
            <template v-slot:title>Test Results</template>
            <template v-slot:actions>
              <Dropdown :ellipsis="true">
                <DropdownEntry>wut</DropdownEntry>
              </Dropdown>
            </template>
            <Vega></Vega>
          </Card>
        </FlexItem>
      </Flex>
    </MainPage>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator'

import MainPage from '@/components/app/MainPage.vue'
import TreeNodeView from '@/components/app/TreeNodeView.vue'

import model from '@/model'
import GeDocumentEditor from "@/components/app/GeDocumentEditor.vue";
import Vega from "@/components/vega/Vega.vue";
import Card from "@germanium-vue-patternfly/Card.vue";
import Dropdown from "@germanium-vue-patternfly/Dropdown.vue";
import DropdownEntry from "@germanium-vue-patternfly/DropdownEntry.vue";
import Flex from "@germanium-vue-patternfly/Flex.vue";
import FlexItem from "@germanium-vue-patternfly/FlexItem.vue";

@Component({
    components: {
      FlexItem,
      Flex,
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
