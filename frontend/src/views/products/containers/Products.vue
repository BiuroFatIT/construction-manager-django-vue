<script setup lang="ts">
import { Config } from '@/types/core/CustomDataTable';
import CustomDataTable from '@/components/core/CustomDataTable.vue';

const configuration: Config[] = [
  {
    field: 'is_active',
    header: 'Aktywny',
    sortable: true,
    filterable: true,
    filterType: 'select',
    filterSelectArray: [
      { label: 'Tak', value: true },
      { label: 'Nie', value: false },
    ],
    body: (row: any) => {
      return `
        <span style="color: ${row.is_active ? 'green' : 'red'}; font-weight: bold; display: flex; align-items: center; gap: 4px;">
          <i class="pi ${row.is_active ? 'pi-check' : 'pi-times'}"></i>
        </span>
      `;
    }
  },
  { field: 'name', header: 'Nazwa', sortable: true, filterable: true, filterType: 'text' },
  { field: 'price_net', header: 'Cenna Netto', sortable: true, filterable: true, filterType: 'number' },
  { field: 'price_gross', header: 'Cenna Brutto', sortable: true, filterable: true, filterType: 'text' },
  { 
    field: 'estimated_duration_weeks', 
    header: 'Czas Budowy', 
    sortable: true, 
    filterable: true, 
    filterType: 'number',
    body: (row: any) => {
      return `
        <span style="color: ${row.estimated_duration_weeks > 50 ? 'red' : 'green'}; font-weight: bold; display: flex; align-items: center; gap: 4px;">
          ${row.estimated_duration_weeks}
        </span>
      `;
    } 
  },
  { field: 'usable_area_m2', header: 'Powierzchnia Użytkowa', sortable: true, filterable: true, filterType: 'number' },
  { field: 'net_area_m2', header: 'Powierzchnia Netto', sortable: true, filterable: true, filterType: 'number' },
  { field: 'gross_volume_m3', header: 'Kubatura', sortable: true, filterable: true, filterType: 'number' },
];
</script>

<template>
    <div class="flex flex-col">
        <CustomDataTable
            url="http://127.0.0.1:8000/api/construction/manager/products/"
            :config="configuration"
        />
    </div>
</template>
