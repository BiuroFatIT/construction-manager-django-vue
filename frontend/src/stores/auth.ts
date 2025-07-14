// src/stores/auth.ts
import { defineStore } from "pinia";
import api from "@/api/apiService";
import { useLocalStorage } from "@vueuse/core";

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  username: string;
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as User | null,
    accessToken: null as string | null,
    refreshToken: null as string | null,
    isAuthReady: false,
  }),
  getters: {
    isLoggedIn: (state) => !!state.user && !!state.accessToken,
  },
  actions: {
    async login(username: string, password: string) {
      const res = await api.post("v1/auth/token/", { username, password });
      this.accessToken = res.data.access;
      this.refreshToken = res.data.refresh;
      localStorage.setItem("access_token", res.data.access);
      localStorage.setItem("refresh_token", res.data.refresh);
      api.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${res.data.access}`;
      await this.fetchUser();
    },
    async fetchUser() {
      try {
        const res = await api.get("v1/auth/users/me/");
        this.user = res.data;
      } catch {
        this.logout();
      }
    },
    logout() {
      this.accessToken = null;
      this.refreshToken = null;
      this.user = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      delete api.defaults.headers.common["Authorization"];
    },
    async initialize() {
      const token = localStorage.getItem("access_token");
      if (token) {
        this.accessToken = token;
        this.refreshToken = localStorage.getItem("refresh_token");
        api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        try {
          await this.fetchUser();
        } catch {
          this.logout();
        }
      }
      this.isAuthReady = true;
    },
  },
});
