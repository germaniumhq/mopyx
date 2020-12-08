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
          {"a": "1", "b": 2, "c": 2},
          {"a": "2", "b": 7, "c": 2},
          {"a": "3", "b": 4, "c": 2},
          {"a": "4", "b": 1, "c": 2},
          {"a": "5", "b": 2, "c": 2},
          {"a": "6", "b": 6, "c": 2},
          {"a": "7", "b": 8, "c": 2},
          {"a": "8", "b": 4, "c": 2},
          {"a": "9", "b": 7, "c": 2}
        ]
      },
      "mark": "line",
      "encoding": {
        "x": {"field": "a", "type": "nominal", "title": "Wut"},
        "y": {"field": "b", "type": "ordinal", "title": "Time"},
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
