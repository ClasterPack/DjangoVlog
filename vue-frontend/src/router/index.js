import { createRouter, createWebHistory } from 'vue-router'
import PagesList from '../views/PagesList.vue'
import PageDetail from '../views/PageDetail.vue'

const routes = [
  { path: '/', name: 'pages', component: PagesList },
  { path: '/pages/:id', name: 'page-detail', component: PageDetail, props: true },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})