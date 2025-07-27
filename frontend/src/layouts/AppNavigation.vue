<!-- src/components/NavigationDrawer.vue -->
<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { navItems } from './navItems'

/* PrimeVue lokalnie (jeśli nie rejestrujesz globalnie przez resolver) */
import Sidebar from 'primevue/sidebar'
import PanelMenu from 'primevue/panelmenu'

/* ───────────────────────────────────────── props / emits ────────────────── */
const props = defineProps<{
  drawer: boolean
  'onUpdate:drawer': (v: boolean) => void
}>()

const emit = defineEmits<{
  (e: 'update:drawer', value: boolean): void
}>()

/* ────────────────────────────── helper: Vuetify → PanelMenu items ────────── */
function mapItems(items: typeof navItems): any[] {
  return items.map((it) => {
    /* Nagłówek sekcji  */
    if ('header' in it) {
      return {
        /* W PanelMenu brak “header”, więc używamy disabled-item’a  */
        label: it.header,
        disabled: true,
        pt: {
          content: { class: 'cursor-default select-none' },
          label:   { class: 'text-xs uppercase tracking-wider text-gray-500 pl-3 pr-2 py-2' },
        },
      }
    }

    /* Element z dziećmi (grupa z aktywatorem) */
    if (it.children) {
      return {
        label: it.title,
        icon:  it.icon?.replace('mdi-', 'pi pi-') ?? undefined,
        items: mapItems(it.children),
      }
    }

    /* Zwykły link  */
    return {
      label: it.title,
      icon:  it.icon?.replace('mdi-', 'pi pi-') ?? undefined,
      to:    it.to,
      command: () => emit('update:drawer', false),  // zamknij szufladę po kliknięciu
    }
  })
}

const menuItems = computed(() => mapItems(navItems))
</script>

<template>
  <!-- LEWA SZUFLADA -->
  <Sidebar
    :visible="drawer"
    position="left"
    class="w-72"
    :showCloseIcon="false"
    @update:visible="emit('update:drawer', $event)"
  >
    <!-- MENU -->
    <PanelMenu
      :model="menuItems"
      class="w-full border-none bg-transparent"
      :pt="{
        menu:   { class: 'bg-transparent' },
        action: { class: 'flex items-center gap-2 px-2 py-2 rounded-md transition-colors hover:bg-primary/10' },
        label:  { class: 'text-sm' },
        icon:   { class: 'text-base' },
      }"
    />
  </Sidebar>
</template>

<style scoped>

</style>
