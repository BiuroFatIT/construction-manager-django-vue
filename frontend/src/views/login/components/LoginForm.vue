<!-- src/components/LoginForm.vue -->
<script setup lang="ts">
/* ────────────────────────── importy ─────────────────────────── */
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToggle } from '@vueuse/core'
import { z } from 'zod';
import {
  Form,
  FormField,
  type FormInstance,
} from '@primevue/forms'
import { zodResolver } from '@primevue/forms/resolvers/zod';
import InputText   from 'primevue/inputtext'
import Password    from 'primevue/password'
import Button      from 'primevue/button'
import Message     from 'primevue/message'

import { useFormRevalidateOnLocale } from '@/core/composables/useFormRevalidateOnLocale'

/* ─────────────────── i18n & typy formularza ─────────────────── */
const { t } = useI18n()

interface LoginFormData {
  username: string
  password: string
}

/* ───────────────────── props / emits ────────────────────────── */
defineProps<{
  loading?: boolean
  error: string | null
}>()

const emit = defineEmits<{
  (e: 'submit', payload: LoginFormData): void
}>()

/* ───────────────────── schema Zod ────────────────────────────── */
const schema = z.object({
  username: z.string().nonempty(t('form.required')),
  password: z.string().nonempty(t('form.required'))
})

/* ───────────────────── stan formularza ───────────────────────── */
const form        = reactive<LoginFormData>({ username: '', password: '' })
const formRef     = ref<FormInstance | null>(null)
const [showPw, togglePw] = useToggle(false)

/* ───────────────────── obsługa submit ───────────────────────── */
async function onSubmit () {
  const result = await formRef.value?.validate()
  if (!result) return
}

/* ────────── re-walidacja po zmianie języka ───────────────────── */
useFormRevalidateOnLocale(formRef)
</script>

<template>
  <Form
    ref="formRef"
    :resolver="zodResolver(schema)"
    @submit.prevent="onSubmit"
    class="flex flex-col gap-4"
  >
    <!-- USERNAME -->
    <FormField name="username" v-slot="$field">
      <label class="block mb-1 font-semibold">{{ t('login.username') }}</label>
      <InputText
        v-model="$field.value"
        :invalid="$field.invalid"
        class="w-full"
        autofocus
        @keyup.enter="onSubmit"
      />
      <Message v-if="$field.invalid" severity="error" size="small">
        {{ $field.error?.message }}
      </Message>
    </FormField>

    <!-- PASSWORD  -->
    <FormField name="password" v-slot="$field">
      <label class="block mb-1 font-semibold">{{ t('login.password') }}</label>
      <div class="relative">
        <Password
          v-model="$field.value"
          :toggleMask="false"
          :feedback="false"
          :input-class="[
            'w-full pr-10',
            $field.invalid && 'p-invalid'
          ]"
          :type="showPw ? 'text' : 'password'"
        />
        <button
          type="button"
          class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-primary-600"
          @click="togglePw()"
          tabindex="-1"
        >
          <i :class="showPw ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
        </button>
      </div>
      <Message v-if="$field.invalid" severity="error" size="small">
        {{ $field.error?.message }}
      </Message>
    </FormField>

    <!-- SUBMIT -->
    <Button
      type="submit"
      :label="t('login.button')"
      :loading="loading"
      icon="pi pi-sign-in"
      class="w-full mt-2"
    />

    <!-- GLOBAL ERROR -->
    <Message v-if="error" severity="error" class="mt-3">
      {{ error }}
    </Message>
  </Form>
</template>
