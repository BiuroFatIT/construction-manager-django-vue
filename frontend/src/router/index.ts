import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import LoginView from '@/views/login/containers/LoginView.vue'
import DashboardView from '@/views/dashboard/containers/DashboardView.vue'

const routes: Array<RouteRecordRaw> = [
  { path: '/login', component: LoginView, name: 'Login', meta: { title: 'Logowanie' } },
  { path: '/', name: 'Home', component: DashboardView , meta: { requiresAuth: true, title: 'Strona główna' } }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Obsługa Vite dynamic import bug (opcjonalne, jeśli potrzebujesz)
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (localStorage.getItem('vuetify:dynamic-reload')) {
      console.error('Dynamic import error, reloading page did not fix it', err)
    } else {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

// Obsługa auth i title 
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !isLoggedIn) {
    next({ path: '/login', query: { next: to.fullPath } })
  } else {
    next()
  }
  const baseTitle = 'Construction Manager'
  document.title = to.meta.title ? to.meta.title as string : baseTitle
})

export default router
