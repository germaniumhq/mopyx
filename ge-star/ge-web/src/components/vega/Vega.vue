<template>
  <div ref="container"></div>
</template>

<script lang="ts">
import { Prop, Vue, Component } from 'vue-property-decorator'
import embed from 'vega-embed'

@Component({})
export default class Vega extends Vue {
  @Prop({})
  data!: any

  $refs!: {
    "container": HTMLElement
  }

  async mounted() {
    const x = await embed(this.$refs.container, {
      "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
      "description": "Basic",
      "data": {
        "values": [
          {"a": "C", "b": 2},
          {"a": "C", "b": 7},
          {"a": "C", "b": 4},
          {"a": "D", "b": 1},
          {"a": "D", "b": 2},
          {"a": "D", "b": 6},
          {"a": "E", "b": 8},
          {"a": "E", "b": 4},
          {"a": "E", "b": 7}
        ]
      },
      "mark": "point",
      "encoding": {
        "x": {"field": "a", "type": "nominal"},
        "y": {"field": "b", "type": "ordinal"}
      }
    }, {
      actions: false,
      renderer: "svg",
      theme: "excel",
    })

    console.log(x)
  }
}
</script>
