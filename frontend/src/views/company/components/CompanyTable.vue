<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="items"
      :items-per-page="5"
      class="elevation-1"
    >
      <template #item.actions="{ item }">
        <v-btn icon @click="editItem(item)">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-btn icon @click="deleteItem(item)">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const headers = ref([
  { text: 'ID', value: 'id' },
  { text: 'Name', value: 'name' },
  { text: 'Email', value: 'email' },
  { text: 'Actions', value: 'actions', sortable: false },
]);

const items = ref([
  { id: 1, name: 'Jan Kowalski', email: 'jan@example.com' },
  { id: 2, name: 'Anna Nowak', email: 'anna@example.com' },
  { id: 3, name: 'Piotr Wiśniewski', email: 'piotr@example.com' },
]);

function editItem(item: any) {
  alert(`Edytujesz: ${item.name}`);
}

function deleteItem(item: any) {
  alert(`Usuwasz: ${item.name}`);
}
</script>