import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Score from '../views/Score.vue'
import Admin from '../views/Admin.vue'
import ScoreStatus from '../views/ScoreStatus.vue'
import ApiTest from '../views/ApiTest.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/score/:taskId/:institutionId',
    name: 'Score',
    component: Score,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/status',
    name: 'ScoreStatus',
    component: ScoreStatus
  },
  {
    path: '/api-test',
    name: 'ApiTest',
    component: ApiTest
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const judge = JSON.parse(localStorage.getItem('judge') || 'null')
  const admin = JSON.parse(localStorage.getItem('admin') || 'null')
  
  if (to.meta.requiresAuth && !judge && !admin) {
    next('/login')
  } else if (to.meta.requiresAdmin && !admin) {
    next('/login')
  } else if (to.path === '/login' && (judge || admin)) {
    if (admin) {
      next('/admin')
    } else {
      next('/home')
    }
  } else {
    next()
  }
})

export default router