<script setup lang="ts">
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: 'Zarządzanie Budową',
        items: [
            { label: 'Produkty', icon: 'pi pi-fw pi-home', to: '/cm/products' },
            { label: 'Dane Firmy', icon: 'pi pi-fw pi-id-card', to: '/cm/company/details' },
            { label: 'Użytkownicy', icon: 'pi pi-fw pi-home', to: '/cm/users' },
        ]
    }
]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>
