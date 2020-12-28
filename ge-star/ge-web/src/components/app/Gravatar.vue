<template>
  <div>
    <Avatar :src="computedHref" :alt="email"/>
  </div>
</template>


<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import Avatar from '@germanium-vue-patternfly/Avatar.vue'
import { createHash } from 'crypto'

@Component({
  components: {
    Avatar,
  }
})
export default class Gravatar extends Vue {
  @Prop() email!: String

  get computedHref() {
      const email = this.email.toLowerCase()
      const digest = createHash('md5').update(email).digest('hex')

      return `https://www.gravatar.com/avatar/${digest}?d=mp`
  }
}
</script>
