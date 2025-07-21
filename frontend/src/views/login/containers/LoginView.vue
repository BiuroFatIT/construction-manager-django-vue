<!-- views/LoginView.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginForm from '../components/LoginForm.vue'
import { useI18n } from 'vue-i18n'
import LanguageSwitcher from '@/core/LanguageSwitcher.vue'
const { t } = useI18n()

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const error = ref<string | null>(null)

function resolveNext(): string {
  const q = route.query.next
  return (Array.isArray(q) ? q[0] : q)?.toString() || '/'
}

async function handleLogin({ username, password }: { username: string; password: string }) {
  error.value = null
  try {
    await auth.login(username, password)
    router.push(resolveNext())
  } catch (e: any) {
    error.value = e.response?.data.detail || e.message || 'Błąd logowania'
  }
}
</script>

<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card width="360" elevation="4">
      <div class="d-flex justify-space-between">
        <v-card-title>{{ t('login.title') }}</v-card-title>
        <LanguageSwitcher />
      </div>
      <v-card-text>
        <LoginForm @submit="handleLogin" :error=error />
      </v-card-text>
    </v-card>
  </v-container>
</template>
