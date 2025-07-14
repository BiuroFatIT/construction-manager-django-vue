<!-- components/LoginForm.vue -->
<script setup lang="ts">
import { reactive, ref } from 'vue'
import { defineEmits, defineProps } from 'vue'
import { useToggle } from '@vueuse/core'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

interface LoginFormData { username: string; password: string }

const emit = defineEmits<{
  (e: 'submit', payload: LoginFormData): void
}>()

const props = defineProps<{
  error: string | null
}>()

const form = reactive<LoginFormData>({ username: '', password: '' })
const isLoading = ref(false)
const [showPassword, toggleShowPassword] = useToggle(false)
const rules = { required: [(v: string) => !!v || 'Pole wymagane'] }

async function onSubmit() {
  isLoading.value = true
  await emit('submit', { ...form })
  isLoading.value = false
}
</script>

<template>
  <v-form @submit.prevent="onSubmit">
    <v-text-field
      v-model="form.username"
      :label="t('login.username')" 
      :rules="rules.required"
      autofocus
      required
      @keyup.enter="onSubmit"
    />
    <v-text-field
      v-model="form.password"
      :type="showPassword ? 'text' : 'password'"
      :label="t('login.password')"
      :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
      @click:append="toggleShowPassword()"
      :rules="rules.required"
      required
      @keyup.enter="onSubmit"
    />
    <v-btn type="submit" :loading="isLoading" color="primary" block class="mt-4">
        {{ t('login.button') }}
    </v-btn>
    <v-alert v-if="props.error" type="error" class="mt-3">
      {{ props.error }}
    </v-alert>
  </v-form>
</template>
