<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import DashboardView from "@/views/dashboard/containers/DashboardView.vue";

const router = useRouter();
const route = useRoute();
const auth = useAuthStore();

const username = ref("");
const password = ref("");
const error = ref<string | null>(null);

async function handleLogin() {
  error.value = null;
  try {
    await auth.login(username.value, password.value);
    const nextUrl = Array.isArray(route.query.next)
      ? route.query.next[0] || "/"
      : route.query.next || "/";
    router.push(nextUrl);
  } catch {
    error.value = "Invalid credentials";
  }
}

</script>

<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card width="350" elevation="3">
      <v-card-title>Log In</v-card-title>
      <v-card-text>
        <v-text-field v-model="username" label="Username" autofocus required />
        <v-text-field
          v-model="password"
          label="Password"
          type="password"
          required
        />
        <v-btn @click="handleLogin" color="primary" block>Log In</v-btn>
        <v-alert v-if="error" type="error" class="mt-2">{{ error }}</v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>
