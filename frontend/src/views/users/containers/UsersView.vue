<script setup lang="tsx">
import { Config } from '@/types/core/CustomDataTable';
import CustomDataTable from '@/components/DataTable/CustomDataTable.vue';
import { defineAsyncComponent } from 'vue';
import Tag from 'primevue/tag';
import Menu from '@/views/users/components/Menu.vue';
import { useDateFormatter } from '@/composable/useDateFormatter';

const { formatDate } = useDateFormatter();
const Form = defineAsyncComponent(() => import('@/views/users/components/UsersForm.vue'));

const configuration: Config[] = [
    {
        field: 'id',
        header: '',
        sortable: false,
        filterable: false,
        filterType: 'text',
        body: (row: any) => <Menu />
    },
    {
        field: 'is_active',
        header: 'Aktywny',
        sortable: true,
        filterable: true,
        filterType: 'select',
        filterSelectArray: [
            { label: 'Tak', value: true },
            { label: 'Nie', value: false }
        ],
        body: (row: any) => (
            <span
                style={{
                    color: row.is_active ? 'green' : 'red',
                    fontWeight: 'bold',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                }}
            >
                <i class={`pi ${row.is_active ? 'pi-check' : 'pi-times'}`}></i>
            </span>
        )
    },
    { field: 'first_name', header: 'Imię', sortable: true, filterable: true, filterType: 'text' },
    { field: 'last_name', header: 'Nazwisko', sortable: true, filterable: true, filterType: 'text' },
    { field: 'email', header: 'Email', sortable: true, filterable: true, filterType: 'text' },
    {
        field: 'groups',
        header: 'Uprawnienia',
        sortable: true,
        filterable: true,
        filterType: 'select',
        filterSelectArray: [
            { label: 'Administrator', value: 'Administrators' },
            { label: 'Architekt', value: 'Architects' },
            { label: 'Klient', value: 'Clients' },
            { label: 'Kierownik Budowy', value: 'ConstructionsManagers' },
            { label: 'Właściciel Firmy', value: 'Owners' },
            { label: 'Geodeta', value: 'Surveyors' },
            { label: 'Pracownik Fizyczny', value: 'Teams' }
        ],
        body: (row: any) => {
            if (!row.groups || row.groups.length === 0) {
                return <Tag severity="danger" value="Brak grup" />;
            }

            return (
                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                    {row.groups.map((group: string) => (
                        <Tag severity={group === 'Owners' ? 'warning' : group === 'Administrators' ? 'success' : 'info'} value={group} />
                    ))}
                </div>
            );
        }
    },
    {
        field: 'last_login',
        header: 'Ostatnie Logowanie',
        sortable: true,
        filterable: true,
        filterType: 'datetime',
        body: (row: any) => <span>{formatDate(row.last_login)}</span>
    },
    { field: 'date_joined', header: 'Data Utworzenia', sortable: true, filterable: true, filterType: 'datetime', body: (row: any) => <span>{formatDate(row.date_joined)}</span> }
];
</script>

<template>
    <div class="flex flex-col">
        <CustomDataTable url="/construction/manager/user/" :config="configuration" :formComponent="Form" />
    </div>
</template>
