<script setup lang="ts">
import { useAuthStore } from './stores/auth';
import ProgressBar from "primevue/progressbar";
const auth = useAuthStore();
auth.initialize();

</script>

<template>
  <div
    v-if="!auth.isAuthReady"
    class="flex items-center justify-center h-screen bg-surface-100"
  >
    <div class="w-full max-w-md text-center px-6">
      <ProgressBar mode="indeterminate" style="height: 6px" class="mb-4" />
      <div class="text-gray-600 text-lg">Ładowanie…</div>
    </div>
  </div>
  <div>
    <router-view />
  </div>
</template>

<style>
  body {
    scrollbar-width: thin; 
    scrollbar-color: rgba(141, 139, 139, 0.2) transparent;
  }
</style>
