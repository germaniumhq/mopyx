<template>
    <MainPage>
        <template v-slot:left_navigation>
          Reports
        </template>

        <div>reports</div>
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
export default class ReportsPage extends Vue {
}
</script>
