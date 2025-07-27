<!-- src/components/TopBar.vue -->
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

/* PrimeVue: lokalne importy (jeśli nie masz resolvera) */
import Toolbar from 'primevue/toolbar'
import Button from 'primevue/button'
import Avatar from 'primevue/avatar'
import Image from 'primevue/image'
import OverlayPanel from 'primevue/overlaypanel'
import Menu from 'primevue/menu'
import Badge from 'primevue/badge'

import fatitLogo from '@/assets/fatit_logo.png'

/* ───────────────────────── props / emits ────────────────────────── */
const props = defineProps<{
  drawer: boolean
  'onUpdate:drawer': (v: boolean) => void
}>()

const emit = defineEmits<{
  (e: 'update:drawer', value: boolean): void
}>()

/* ───────────────────────────── stores / router ───────────────────── */
const auth   = useAuthStore()
const router = useRouter()

const username = computed(() => auth.user?.username ?? 'User')
const avatar   = computed(() => auth.user?.avatar ??
  'https://randomuser.me/api/portraits/men/85.jpg')

/* ───────────────────────────── motywy ───────────────────────────── */
type ThemeKey = 'light' | 'dark' | 'grey-orange' | 'violet'
const currentTheme = ref<ThemeKey>('light')

const themes: { value: ThemeKey; label: string; icon: string }[] = [
  { value: 'light',      label: 'Jasny',   icon: 'pi-sun'   },
  { value: 'dark',       label: 'Ciemny',  icon: 'pi-moon'  },
  { value: 'grey-orange',label: 'Grey-Orange', icon: 'pi-palette' },
  { value: 'violet',     label: 'Violet',  icon: 'pi-palette' },
]

function setTheme(name: ThemeKey) {
  currentTheme.value = name
  localStorage.setItem('theme', name)
  /* tutaj możesz przełączyć plik CSS/tokenty – zależnie od implementacji */
}

/* załaduj motyw z localStorage przy starcie */
onMounted(() => {
  const saved = localStorage.getItem('theme') as ThemeKey | null
  if (saved) currentTheme.value = saved
})

/* ───────────────────────────── akcje ────────────────────────────── */
function handleLogout() {
  auth.logout()
  router.push('/login')
}
function toggleDrawer() {
  emit('update:drawer', !props.drawer)
}

/* ───────────── refy do OverlayPanel / Menu (PrimeVue API) ───────── */
const themePanel = ref<InstanceType<typeof OverlayPanel> | null>(null)
const userMenu   = ref<InstanceType<typeof Menu> | null>(null)

function openTheme(e: Event) {
  themePanel.value?.toggle(e)
}
function openUserMenu(e: Event) {
  userMenu.value?.toggle(e)
}

/* user-menu items */
const userMenuItems = [
  { label: 'Dashboard',    icon: 'pi pi-home',      command: () => router.push('/user/dashboard') },
  { label: 'Notifications',icon: 'pi pi-bell',      command: () => router.push('/notifications') },
  { label: 'Settings',     icon: 'pi pi-cog',       command: () => router.push('/settings') },
  { separator: true },
  { label: 'Logout',       icon: 'pi pi-sign-out',  class: 'text-red-600', command: handleLogout },
]
</script>

<template>
  <!-- TOOLBAR -->
  <Toolbar class="fixed top-0 left-0 w-full z-50 shadow-sm h-16 px-2">
    <!-- LEFT -->
    <template #start>
      <div class="flex items-center gap-2">
        <!-- Hamburger -->
        <Button
          icon="pi pi-bars"
          rounded
          text
          aria-label="Menu"
          @click="toggleDrawer"
        />

        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2 no-underline">
          <Image :src="fatitLogo" alt="logo" class="w-8 h-8" />
          <span class="font-semibold text-lg text-primary-600">FatIT</span>
        </RouterLink>
      </div>
    </template>

    <!-- RIGHT -->
    <template #end>
      <div class="flex items-center gap-2">
        <!-- Notifications -->
        <Button
          icon="pi pi-bell"
          rounded
          text
          aria-label="Powiadomienia"
        >
          <Badge severity="danger" class="absolute -top-1 -right-1 h-2 w-2" />
        </Button>

        <!-- Settings -->
        <Button
          icon="pi pi-cog"
          rounded
          text
          aria-label="Ustawienia"
          @click="router.push('/settings')"
        />

        <!-- Theme picker -->
        <Button
          icon="pi pi-palette"
          rounded
          text
          aria-label="Motyw"
          @click="openTheme($event)"
        />

        <!-- User menu -->
        <Button
          rounded
          text
          aria-label="User menu"
          @click="openUserMenu($event)"
        >
          <Avatar :image="avatar" shape="circle" class="w-9 h-9" />
        </Button>
      </div>
    </template>
  </Toolbar>

  <!-- OverlayPanel: wybór motywu -->
  <OverlayPanel ref="themePanel" :showCloseIcon="false" class="p-0 shadow-lg">
    <ul class="w-56">
      <li
        v-for="t in themes"
        :key="t.value"
        @click="setTheme(t.value); themePanel?.hide()"
        class="flex items-center gap-3 px-3 py-2 cursor-pointer hover:bg-primary/10"
        :class="currentTheme === t.value && 'font-semibold text-primary-600'"
      >
        <i :class="['pi', t.icon]"></i>
        {{ t.label }}
      </li>
    </ul>
  </OverlayPanel>

  <!-- Menu PrimeVue: user menu -->
  <Menu ref="userMenu" :model="userMenuItems" popup />
</template>

<style scoped>
/* Toolbar domyślnie ma display:flex od PrimeVue – wystarczy */
</style>
