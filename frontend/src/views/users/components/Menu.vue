<script lang="ts" setup>
import { ref } from 'vue';
import { useDialog } from 'primevue/usedialog';

const Form = defineAsyncComponent(() => import('@/views/users/components/UsersForm.vue'));

const dialog = useDialog();

const showAddDialog = () => {
    const dialogRef = dialog.open(Form, {
        props: {
            header: 'Edytuj Rekord',
            modal: true
        },
        templates: {},
        onClose: () => {}
    });
};

const menu = ref();
const items = ref([
    {
        label: 'Edit',
        icon: 'pi pi-file-edit',
        command: () => {
            showAddDialog();
        }
    }
]);

const toggle = (event) => {
    menu.value.toggle(event);
};
</script>

<template>
    <Button type="button" severity="secondary" icon="pi pi-bars" class="p-button-rounded p-button-text" @click="toggle" aria-haspopup="true" aria-controls="overlay_tmenu" />
    <TieredMenu ref="menu" id="overlay_tmenu" :model="items" popup />
</template>
