// src/stores/auth.ts
import { defineStore } from 'pinia'
import api from '@/api/apiService'

interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  is_active: boolean
  username: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: !!localStorage.getItem('access_token'),
    accessToken: localStorage.getItem('access_token') as string | null,
    refreshToken: localStorage.getItem('refresh_token') as string | null,
    user: null as User | null,
  }),
  actions: {
    async login(username: string, password: string) {
      const res = await api.post('v1/auth/token/', { username, password })
      this.accessToken = res.data.access
      this.refreshToken = res.data.refresh
      this.isLoggedIn = true
      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh)
      api.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`
      await this.fetchUser()
    },
    async fetchUser() {
      try {
        const res = await api.get('v1/auth/users/me/')
        this.user = res.data
        this.isLoggedIn = true
      } catch (e) {
        this.user = null
        this.isLoggedIn = false
        this.accessToken = null
        this.refreshToken = null
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        delete api.defaults.headers.common['Authorization']
      }
    },
    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.isLoggedIn = false
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      delete api.defaults.headers.common['Authorization']
    },
    async initialize() {
      this.accessToken = localStorage.getItem('access_token')
      this.refreshToken = localStorage.getItem('refresh_token')
      if (this.accessToken) {
        api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
        await this.fetchUser()
      } else {
        this.isLoggedIn = false
        this.user = null
        delete api.defaults.headers.common['Authorization']
      }
    },
    watchStorage() {
      window.addEventListener('storage', (event) => {
        if (event.key === 'access_token' || event.key === 'refresh_token') {
          this.initialize()
        }
      })
    }
  },
})
