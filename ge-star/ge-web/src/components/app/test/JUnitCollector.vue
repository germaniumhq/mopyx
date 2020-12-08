<template>
  <Tabs :secondary="true">
    <template v-slot:tabs>
      <Tab active="true">description</Tab>
      <Tab>config</Tab>
    </template>

    <div class="content">
      some content
    </div>

  </Tabs>
</template>

<script lang="ts">
import { Prop, Vue, Component } from 'vue-property-decorator'
import Tabs from "@/components/patternfly/Tabs.vue";
import Tab from "@/components/patternfly/Tab.vue";

@Component({
  components: {
    Tabs,
    Tab,
  }
})
export default class JUnitCollector extends Vue {
}
</script>

<style type="scss">
div.content {
  background-color: white;
}
</style>