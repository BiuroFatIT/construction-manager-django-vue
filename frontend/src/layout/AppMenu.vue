<script setup lang="ts">
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: 'Constraction Manager',
        items: [
            { label: 'Firmy', icon: 'pi pi-fw pi-id-card', to: '/cm/companies' },
            { label: 'Produkty', icon: 'pi pi-fw pi-home', to: '/cm/products' },
        ]
    },
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
