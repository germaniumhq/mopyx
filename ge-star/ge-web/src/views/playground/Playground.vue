<template>
  <div>
    <div class="data" ref="data"></div>
    <div>content</div>
    <div>content</div>
    <div>content</div>
    <div>content</div>
    <div>content</div>
    <div>content</div>
    <div>content</div>
    <div>content</div>
    <div>content</div>
    <button id="send-echo-request" @click="sendEchoRequest">send echo request</button>
    <button id="send-repeat-request" @click="sendRepeatRequest">send repeat request</button>
    <input id="some-text" name="a" type="text"/>
    <Tooltip for="#send-echo-request" position="top">Send a single request to the server</Tooltip>
    <Tooltip for="#send-repeat-request" position="bottom">Send a repeated request to the server. Send a repeated request to the server.Send a repeated request to the server.</Tooltip>
    <Tooltip for="#some-text" position="left">send some data</Tooltip>
  </div>
</template>

<script lang="ts">
import {EchoClient} from './echo_pb_service'
import {EchoMessage} from './echo_pb'
import {Component, Vue} from 'vue-property-decorator'
import * as oaas from "@/model/oaas";
import Tooltip from "@/components/patternfly/Tooltip.vue";


@Component({
  components: {
    Tooltip: Tooltip,
  }
})
export default class Playground extends Vue {
  $refs!: {
    data: HTMLButtonElement,
  }

  async sendEchoRequest() {
    const c = oaas.client(EchoClient, {instance: "custom"})

    try {
      let echoMessage = new EchoMessage()
      echoMessage.setMsg("x")

      const data = await oaas.asPromise<EchoMessage, EchoMessage>(c, EchoClient.prototype.echo)(echoMessage);

      this.$refs.data.innerHTML = data?.getMsg()
    } catch (err) {
      this.$refs.data.innerHTML = `error ${err}`
      console.log(err);
    }
  }

  sendRepeatRequest() {
    const client = oaas.client(EchoClient);
    let message = new EchoMessage();
    message.setMsg("test")

    const repeat = client.repeat(message)

    repeat.on("data", (message) => {
      this.$refs.data.innerHTML = message.getMsg()
    })
    repeat.on("status", (status) => {
      console.log(`status is ${status}`)
    })
  }
}
</script>
