<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<!-- eslint-disable @typescript-eslint/no-unused-vars -->
<script lang="ts" setup>
  import { ref, onMounted, h, watch } from 'vue';
  import type { Component } from 'vue';
  import { DataTable, 
    Column, 
    DataTablePageEvent, 
    DataTableSortEvent, 
    Button, 
    InputText, 
    InputIcon, 
    IconField, 
    InputNumber, 
    MultiSelect, 
    useDialog,
    DatePicker} from 'primevue';
  import { Config, FilterItem } from '@/types/core/CustomDataTable';
  import api from '@/api/apiService';
    
  const props = defineProps<{
    formComponent: Component;
    config: Config[];
    url: string;
  }>();

  const items = ref<any[]>([]);
  const rows = ref<number>(15);
  const page = ref<number>(1);
  const globalFilter = ref('');
  const totalRecords = ref<number>(0);
  const sortField = ref<string | number | symbol | ((item: any) => string) | undefined>(undefined);
  const sortOrder = ref<number | undefined>(undefined);
  const loading = ref<boolean | false>(false)



  function convertFilterKeys(filters: Record<string, any>): Record<string, any> {
    const newFilters: Record<string, any> = {};
    Object.entries(filters).forEach(([key, val]) => {
      const newKey = key.replace(/\./g, '__');
      newFilters[newKey] = val;
    });
    return newFilters;
  }

  async function fetchData() {
    try {
      loading.value = true;
      const params: Record<string, any> = {
        // Pagination
        page: page.value,
        page_size: rows.value
      };

      // Sorting
      if (sortField.value) {
        params.ordering = sortOrder.value === -1 ? `-${String(sortField.value)}` : sortField.value;
      }

      // Filtering - przygotuj obiekt prosty z polami i ich wartościami (pomijając matchMode)
      const simpleFilters = Object.fromEntries(
        Object.entries(filters.value).map(([field, filter]) => [field, filter.value])
      );

      // Przygotowane pod joiny django
      const djangoFilters = convertFilterKeys(simpleFilters);

      // Dodaj sformatowane filtry do params
      Object.assign(params, flattenFiltersWithBracketKeys(djangoFilters));

      if (globalFilter.value) {
        params.search = globalFilter.value;
      }

      const response = await api.get(props.url, { params });

      items.value = response.data.results;
      totalRecords.value = response.data.count;
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      loading.value = false;
    }
  }

  onMounted(() =>{
    fetchData();
  })

  // Pagination Handler
  function onPage(e: DataTablePageEvent) {
    page.value = e.page + 1;
    rows.value = e.rows;
    fetchData();
  }

  // Sorting Handler
  function onSort(event: DataTableSortEvent) {
    sortField.value = event.sortField as string;
    sortOrder.value = event.sortOrder as number;
    page.value = 1;
    fetchData();
  }

  // Filters Handler
  const filters = ref<Record<string, FilterItem>>({});

  function onFilterChange() {
    page.value = 1; 
    fetchData();
  }

  props.config.forEach((col) => {
    if (!col.filterable) return

    let matchMode = 'contains'
    if (col.filterType === 'number') matchMode = 'equals'
    if (col.filterType === 'select') matchMode = 'in'

    filters.value[col.field] = { value: null, matchMode }
  })

  function getFilterComponent(col: any, filterModel: any, filterCallback: any) {
    const filterItem = filters.value[col.field];

    // Synchronizacja filterModel.value <-> filters.value[col.field].value
    watch(
      () => filterModel.value,
      (newVal) => {
        filterItem.value = newVal;

        const isCleared =
          newVal === null ||
          (Array.isArray(newVal) && newVal.length === 0) ||
          (typeof newVal === 'object' && newVal !== null && Object.values(newVal).every(v => v == null));

        if (isCleared) {
          filterCallback(); // 🔁 triggeruj filtr ręcznie przy „Clear”
        }
      }
    );

    if (col.filterType === 'text') {
      return h(InputText, {
        modelValue: filterItem.value,
        'onUpdate:modelValue': (val: any) => {
          filterItem.value = val;
          filterModel.value = val;
        },
        placeholder: 'Szukaj',
        class: 'p-column-filter'
      });
    }

    if (col.filterType === 'number') {
      return h('div', {
        class: 'p-column-filter-range',
        style: { display: 'flex', gap: '0.5rem', alignItems: 'center' }
      }, [
        h(InputNumber, {
          modelValue: filterModel.value?.[`min`],
          'onUpdate:modelValue': (val: any) => {
            filterModel.value = { ...filterModel.value, [`min`]: val };
          },
          placeholder: 'Min',
          inputStyle: { width: '85px' },
          class: 'p-column-filter',
          mode: 'decimal',
          minFractionDigits: 0,
          maxFractionDigits: 2
        }),
        h(InputNumber, {
          modelValue: filterModel.value?.[`max`],
          'onUpdate:modelValue': (val: any) => {
            filterModel.value = { ...filterModel.value, [`max`]: val };
          },
          placeholder: 'Max',
          inputStyle: { width: '85px' },
          class: 'p-column-filter',
          mode: 'decimal',
          minFractionDigits: 0,
          maxFractionDigits: 2
        })
      ]);
    }

    if (col.filterType === 'select') {
      return h(MultiSelect, {
        modelValue: filterModel.value,
        'onUpdate:modelValue': (val: any) => {
          filterModel.value = val;
        },
        options: col.filterSelectArray,
        optionLabel: 'label',
        optionValue: 'value',
        placeholder: 'Filtruj...',
        class: 'p-column-filter'
      });
    }

    if (col.filterType === 'date' || col.filterType === 'datetime') {
      return h(DatePicker, {
        'onUpdate:modelValue': (val: any) => {
          if (Array.isArray(val)) {
            // Zakres dat
            filterModel.value = val.map(date => date ? formatDate(date) : null);
          } else {
            // Pojedyncza data
            filterModel.value = val ? formatDate(val) : null;
          }
        },
        placeholder: col.filterType === 'datetime' ? 'Wybierz datę i godzinę' : 'Wybierz datę',
        class: 'p-column-filter',
        showTime: col.filterType === 'datetime',
        hourFormat: '24',
        selectionMode: 'range',
        rangeSeparator: ' do ',
        dateFormat: 'yy-mm-dd',
        showIcon: true
      });
    }

    return null;
  }

  function formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0'); // miesiące od 0
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  function formatFilterValue(value: any) {
    if (value instanceof Date) {
      return value.toISOString().split('T')[0];
    }
    return value;
  }

  // Nowa funkcja, która formatuje filtry i zamienia nawiasy na _
  function flattenFiltersWithBracketKeys(filters: any) {
    const params: Record<string, any> = {};

    Object.entries(filters).forEach(([key, filter]) => {
      if (filter && typeof filter === 'object' && !Array.isArray(filter)) {
        // Jeśli wartość to obiekt (np. { min: 500, max: 600 })
        Object.entries(filter).forEach(([subKey, val]) => {
          const newKey = `${key}_${subKey}`;
          params[newKey] = formatFilterValue(val);
        });
      } else {
        // Jeśli klucz ma nawiasy, np. "id[min]"
        const newKey = key.replace(/\[(.+?)\]/g, '_$1');
        params[newKey] = formatFilterValue(filter);
      }
    });

    return params;
  }

  let globalFilterTimeout: ReturnType<typeof setTimeout>;
  function onGlobalFilterChange() {
    clearTimeout(globalFilterTimeout);
    globalFilterTimeout = setTimeout(() => {
      page.value = 1;
      fetchData();
    }, 500);
  }

  function clearFilters() {
    Object.keys(filters.value).forEach(key => {
      filters.value[key].value = null;
    });

    page.value = 1;
    globalFilter.value = '';
    fetchData();
  }

  // Dialog Configuration Add New Rekord
  const dialog = useDialog();

  const showAddDialog = () => {
      const dialogRef = dialog.open(props.formComponent, {
          props: {
            header: 'Dodaj Rekord',
            modal: true
          },
          templates: {
          },
          onClose: () => {
          }
      });
  }
</script>

<template>
  <DataTable 
    :value="items"
    :totalRecords="totalRecords"
    lazy
    selectionMode="single"
    removableSort @sort="onSort" :sortField="sortField" :sortOrder="sortOrder"
    resizableColumns columnResizeMode="expand"
    paginator :rowsPerPageOptions="[5, 15, 30, 50, 100]" :rows="rows" @page="onPage"
    stripedRows showGridlines
    filterDisplay="menu" :filters="filters"
    :loading="loading"
    @filter="onFilterChange"
    scrollable scrollHeight="75vh"
    >
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <Button icon="pi pi-external-link" outlined label="Export" style="margin-right: 10px;"/>
          <Button icon="pi pi-plus" outlined label="Dodaj Rekord" @click="showAddDialog" />
          <DynamicDialog />
        </div>
       
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <Button type="button" icon="pi pi-filter-slash" label="Clear" outlined style="margin-right:10px;" @click="clearFilters"/>
          <IconField>
            <InputIcon>
              <i class="pi pi-search" />
            </InputIcon>
            <InputText
              v-model="globalFilter"
              placeholder="Global Search"
              @input="onGlobalFilterChange"
            />
          </IconField>
        </div>
      </div>
    </template>
    <Column
      v-for="(config, index) in props.config"
      :key="index"
      :field="config.field"
      :header="config.header"
      :sortable="config.sortable"
      :filter="true"
      :showFilterMenu="true"
      :showFilterMatchModes="false"
    >
      <template v-if="config.body" #body="{ data }">
        <component :is="config.body(data)" />
      </template>
      <template #filter="{ filterModel, filterCallback }">
        <component :is="getFilterComponent(config, filterModel, filterCallback)" />
      </template>
    </Column>
  </DataTable>
</template>