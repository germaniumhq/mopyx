import router from './router'
import Vue from 'vue'
import App from './App.vue'


require('@patternfly/patternfly/patternfly.scss')

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
