<template>
    <i :class="cssClasses" @click="onClick"></i>
</template>

<style scoped>
.fas {
    margin: 0 0.2em
}
</style>


<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component({})
export default class Icon extends Vue {
    @Prop() icon!: string
    @Prop() _class!: string

    get cssClasses() {
        return `fas ${this.icon} ${this._class}`
    }

    onClick() {
/* eslint no-console: ["off", { allow: ["warn", "error"] }] */
        console.log("click icon")
        this.$emit("click")
    }
}
</script>
