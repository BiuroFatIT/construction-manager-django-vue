// src/stores/auth.ts
import { defineStore } from 'pinia';
import api from '@/api/apiService';
import { useLocalStorage } from '@vueuse/core';
import axios from 'axios';

interface User {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    is_active: boolean;
    avatar: string;
    username: string;
}

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null as User | null, 
        accessToken: useLocalStorage<string | null>('access_token', null),
        refreshToken: useLocalStorage<string | null>('refresh_token', null),
        isAuthReady: false
    }),
    getters: {
        isLoggedIn: (state) => !!state.user && !!state.accessToken
    },
    actions: {
        async login(username: string, password: string) {
            const res = await api.post('v1/auth/token/', { username, password });

            this.accessToken = res.data.access;
            this.refreshToken = res.data.refresh;

            api.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`;
            await this.fetchUser();
        },
        async fetchUser() {
            try {
                const res = await api.get('v1/auth/users/me/');
                this.user = res.data;
            } catch (error) {
                console.error('Failed to fetch user:', error);
                throw error;
            }
        },
        logout() {
            this.accessToken = null;
            this.refreshToken = null;
            this.user = null;
            delete api.defaults.headers.common['Authorization'];
        },
        async tryRefreshToken() {
            if (!this.refreshToken) {
                return false;
            }
            try {
                const { data } = await axios.post('http://localhost:8000/api/v1/auth/token/refresh/', {
                    refresh: this.refreshToken
                });

                this.accessToken = data.access;
                if (data.refresh) {
                    this.refreshToken = data.refresh;
                }
                api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`;
                await this.fetchUser();

                return true;
            } catch (e) {
                this.logout();
                return false;
            }
        },
        async initialize() {
            const token = this.accessToken;
            if (token) {
                api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                try {
                    await this.fetchUser();
                } catch {
                }
            }
            else if (this.refreshToken) {
                try {
                    const refreshed = await this.tryRefreshToken();
                    if (refreshed) await this.fetchUser();
                } catch {}
            }

            this.isAuthReady = true;
        }
    }
});
