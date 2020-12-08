import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'overview',
    component: () => import(/* webpackChunkName: "overview" */ '../views/overview/Overview.vue')
  },
  {
    path: '/tests',
    name: 'tests',
    component: () => import(/* webpackChunkName: "projects" */ '../views/tests/Tests.vue')
  },
  {
    path: '/data',
    name: 'data',
    component: () => import(/* webpackChunkName: "data" */ '../views/data/DataPage.vue')
  },
  {
    path: '/reports',
    name: 'report',
    component: () => import(/* webpackChunkName: "reports" */ '../views/reports/ReportsPage.vue')
  },
  {
    path: '/playground',
    name: 'playground',
    component: () => import(/* webpackChunkName: "playground" */ '../views/playground/Playground.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
