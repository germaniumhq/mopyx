import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'overview',
    component: () => import(/* webpackChunkName: "about" */ '../views/overview/Overview.vue')
  },
  {
    path: '/projects',
    name: 'projects',
    component: () => import(/* webpackChunkName: "about" */ '../views/projects/Projects.vue')
  },
  {
    path: '/data',
    name: 'data',
    component: () => import(/* webpackChunkName: "about" */ '../views/data/DataPage.vue')
  },
  {
    path: '/reports',
    name: 'report',
    component: () => import(/* webpackChunkName: "about" */ '../views/reports/ReportsPage.vue')
  },
  {
    path: '/playground',
    name: 'playground',
    component: () => import(/* webpackChunkName: "about" */ '../views/playground/Playground.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
