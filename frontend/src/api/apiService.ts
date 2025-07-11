import axios from 'axios'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
})

// Interceptor do obsługi automatycznego refreshu JWT po 401
api.interceptors.response.use(
  response => response,
  async error => {
    const auth = useAuthStore()
    const originalRequest = error.config

    // Jeżeli 401, mamy refresh token i jeszcze nie próbowaliśmy odświeżyć
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem('refresh_token')
    ) {
      originalRequest._retry = true
      try {
        // Wywołujemy endpoint refresh
        const res = await api.post('/v1/auth/token/refresh/', {
          refresh: localStorage.getItem('refresh_token'),
        })
        // Ustawiamy nowy access token
        localStorage.setItem('access_token', res.data.access)
        api.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`
        originalRequest.headers['Authorization'] = `Bearer ${res.data.access}`

        // Odśwież token także w store!
        auth.accessToken = res.data.access

        // Powtarzamy request
        return api(originalRequest)
      } catch (refreshError) {
        // Jeśli refresh token też nie działa – wyloguj usera
        auth.logout()
        router.push({ name: 'Login', query: { next: router.currentRoute.value.fullPath } })
      }
    }

    // Każdy inny błąd (albo już próbowaliśmy refresh) – normalny reject
    return Promise.reject(error)
  }
)

export default api
