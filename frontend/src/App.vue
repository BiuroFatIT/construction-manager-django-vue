<script setup lang="ts">
import { ref } from "vue";
import AppNavigation from "@/layouts/AppNavigation.vue";
import AppBar from "@/layouts/AppBar.vue";
import { RouterView } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const drawer = ref(true);
const auth = useAuthStore();

auth.initialize();
</script>

<template>
  <div v-if="!auth.isAuthReady">
    <v-container
      class="d-flex align-center justify-center"
      style="height: 100vh"
      fluid
    >
      <v-col cols="6" class="text-center">
        <v-progress-linear
          height="6"
          indeterminate
          rounded
        />
        <div class="mt-4" style="font-size: 1.2rem; color: #666;">
          Ładowanie...
        </div>
      </v-col>
    </v-container>
  </div>
  <v-app v-else>
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
    <v-main>
      <v-container fluid class="py-6">
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>
