import axios from "axios";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import { useLanguageStore } from "@/stores/language";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

// Interceptor do ustawiania nagłówków z językiem i tokenem
api.interceptors.request.use((config) => {
  const langStore = useLanguageStore();

  config.headers = config.headers || {};
  config.headers["Accept-Language"] = langStore.selected;

  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }

  return config;
});

// Interceptor do obsługi automatycznego odświeżania JWT po 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const auth = useAuthStore();

    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem("refresh_token")
    ) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh_token");

        const { data } = await api.post("/v1/auth/token/refresh/", {
          refresh: refreshToken,
        });

        localStorage.setItem("access_token", data.access);
        api.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;
        originalRequest.headers["Authorization"] = `Bearer ${data.access}`;

        // Aktualizuj token w store
        auth.accessToken = data.access;

        return api(originalRequest);
      } catch (refreshError) {
        auth.logout();
        router.push({
          name: "Login",
          query: { next: router.currentRoute.value.fullPath },
        });
      }
    }

    return Promise.reject(error);
  }
);

export default api;
