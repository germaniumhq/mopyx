<template>
  <div>
    <div class="data" ref="data"></div>
    <button @click="sendEchoRequest">send echo request</button>
    <button @click="sendRepeatRequest">send repeat request</button>
  </div>
</template>

<script lang="ts">
import {EchoClient, ServiceError, UnaryResponse} from './echo_pb_service'
import { EchoMessage } from './echo_pb'
import {grpc} from "@improbable-eng/grpc-web";
import { Vue, Component } from 'vue-property-decorator'

function p<S, R>(
    that: any,
    fn: (data: S, metadata: grpc.Metadata, callback: (err: ServiceError|null, resp: R|null) => void) => UnaryResponse,
): (data: S, metadata: grpc.Metadata) => Promise<R> {
// S=sent, R=response, UR=unary response
  function _call(data: S, metadata: grpc.Metadata|null): Promise<R> {
    return new Promise((resolve, reject) => {
      const args: any = [data]

      if (metadata) {
        args.push(metadata);
      }

      args.push((err: Error|null, result: R) => {
        if (err) {
          reject(err);
          return;
        }

        resolve(result);
      })

      fn.apply(that, args)
    });
  }

  return _call;
}

@Component({})
export default class Playground extends Vue {
  $refs!: {
    data: HTMLButtonElement,
  }

  async sendEchoRequest() {
    const client = new EchoClient("http://localhost:9000")

    try {
      console.log("x");
      let metadata = new grpc.Metadata({
        'x-oaas-auth': 'abcd',
        'x-oaas-route': JSON.stringify({
          'custom': 'structure',
          'is': ['here']
        })
      });
      let echoMessage = new EchoMessage()
      echoMessage.setMsg("x")
      const data = await p<EchoMessage, EchoMessage>(client, client.echo)(echoMessage, metadata)

      this.$refs.data.innerHTML = data?.getMsg()
    } catch (err) {
      this.$refs.data.innerHTML = `error ${err}`
      console.log(err);
    }
  }

  sendRepeatRequest() {
    const client = new EchoClient("http://localhost:9000")
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
