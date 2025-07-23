<!-- components/LoginForm.vue -->
<script setup lang="ts">
import { reactive, ref } from "vue";
import { useToggle } from "@vueuse/core";
import { useI18n } from "vue-i18n";
const { t } = useI18n();
import { useFormRevalidateOnLocale } from "@/core/composables/useFormRevalidateOnLocale";

interface LoginFormData {
  username: string;
  password: string;
}

const emit = defineEmits<{
  (e: "submit", payload: LoginFormData): void;
}>();

const props = defineProps<{
  loading?: boolean;
  error: string | null;
}>();

const form = reactive<LoginFormData>({ username: "", password: "" });
const isLoading = ref(false);
const [showPassword] = useToggle(false);
const formRef = ref();

import { computed } from 'vue'

const rules = computed(() => ({
  required: [(v: string) => !!v || t('form.required')],
}));

async function onSubmit() {
  const isValid = await formRef.value.validate();
  if (!isValid.valid) return;
  
  isLoading.value = true;
  emit("submit", { ...form });
  isLoading.value = false;
}

useFormRevalidateOnLocale(formRef);
</script>

<template>
  <v-form ref="formRef" @submit.prevent="onSubmit">
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
      :rules="rules.required"
    >
      <template #append-inner>
        <v-tooltip
          :text="
            showPassword ? t('login.hide_password') : t('login.show_password')
          "
        >
          <template #activator="{ props }">
            <v-btn
              icon
              v-bind="props"
              variant="plain"
              tabindex="-1"
              @click="showPassword = !showPassword"
            >
              <v-icon>
                {{ showPassword ? "mdi-eye-off" : "mdi-eye" }}
              </v-icon>
            </v-btn>
          </template>
        </v-tooltip>
      </template>
    </v-text-field>
    <v-btn
      type="submit"
      :loading="props.loading"
      color="primary"
      block
      class="mt-4"
    >
      {{ t("login.button") }}
    </v-btn>
    <v-alert v-if="props.error" type="error" class="mt-3">
      {{ props.error }}
    </v-alert>
  </v-form>
</template>
