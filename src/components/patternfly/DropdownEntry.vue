<template>
    <li>
      <a :class="cssClasses" 
          href="#"
          @click="onClick"
          :aria-disabled="disabled"
          :tabindex="tabindex"><slot></slot></a>
    </li>    
</template>

<script lang="ts">
import { Vue, Component, Prop} from 'vue-property-decorator'

@Component({})
export default class DropdownEntry extends Vue {
    @Prop({default: false}) disabled! : boolean;

    get cssClasses() {
        return {
            "pf-c-dropdown__menu-item": true,
            "pf-m-disabled": this.disabled
        }
    }

    get tabindex() {
        if (this.disabled) {
            return "-1";
        }

        return false;
    }

    onClick() {
        if (this.disabled) {
            return;
        }

        this.$emit("click")
    }
}
</script>
