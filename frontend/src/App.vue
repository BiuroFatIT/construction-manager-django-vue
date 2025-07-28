<!-- src/App.vue -->
<script setup lang="ts">
import { ref } from "vue";
import { RouterView } from "vue-router";
import AppNavigation from "@/layouts/AppNavigation.vue";
import AppBar from "@/layouts/AppBar.vue";
import { useAuthStore } from "@/stores/auth";

/* PrimeVue komponent postępu */
import ProgressBar from "primevue/progressbar";

const drawer = ref(true);
const auth = useAuthStore();

auth.initialize(); // odpal Init auth na starcie
</script>

<template>
  <!-- EKRAN ŁADOWANIA (do czasu aż auth.isAuthReady) -->
  <div
    v-if="!auth.isAuthReady"
    class="flex items-center justify-center h-screen bg-surface-100"
  >
    <div class="w-full max-w-md text-center px-6">
      <ProgressBar mode="indeterminate" style="height: 6px" class="mb-4" />
      <div class="text-gray-600 text-lg">Ładowanie…</div>
    </div>
  </div>

  <!-- GŁÓWNY LAYOUT -->
  <div v-else class="min-h-screen flex flex-col">
    <!-- Sidebar + TopBar tylko dla zalogowanego -->
    <AppNavigation
      v-if="auth.isLoggedIn"
      :drawer="drawer"
      @update:drawer="drawer = $event"
    />
    <AppBar
      v-if="auth.isLoggedIn"
      :drawer="drawer"
      @update:drawer="drawer = $event"
    />
    <!-- Zawartość routingu -->
    <main>
      <RouterView />
    </main>
  </div>
</template>
