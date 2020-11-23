<template>
  <div>
    <div class="data" ref="data"></div>
    <button @click="sendEchoRequest">send echo request</button>
    <button @click="sendRepeatRequest">send repeat request</button>
  </div>
</template>

<script lang="ts">
import {EchoClient} from './echo_pb_service'
import {EchoMessage} from './echo_pb'
import {Component, Vue} from 'vue-property-decorator'
import * as oaas from "@/model/oaas";


@Component({})
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
