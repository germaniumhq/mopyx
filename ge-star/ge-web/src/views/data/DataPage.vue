<template>
    <MainPage>
        <template slot="left_navigation">
            data navigation
        </template>

        <div>data</div>
    </MainPage>
</template>

<script lang="ts">
import MainPage from '@/components/app/MainPage.vue'

import { Vue, Component } from 'vue-property-decorator'
import model from '@/model'

@Component({
    components: {
        MainPage,
    }
})
export default class DataPage extends Vue {
}
</script>