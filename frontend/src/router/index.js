import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import DataList from '../pages/DataList.vue'
import DataView from '../pages/DataView.vue'
import AdminDashboard from '../pages/AdminDashboard.vue'
import LoginPage from '../pages/LoginPage.vue'
import UpgradePage from '../pages/UpgradePage.vue'

const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/login', name: 'login', component: LoginPage },
  { path: '/data', name: 'data-list', component: DataList },
  { path: '/data/:id', name: 'data-view', component: DataView, props: true },
  { path: '/upgrade', name: 'upgrade', component: UpgradePage },
  { path: '/admin', name: 'admin', component: AdminDashboard }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
