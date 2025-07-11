<script setup lang="ts">
const kpis = [
  { label: 'Aktywne Projekty', icon: 'mdi-domain', value: 14, color: 'primary' },
  { label: 'Ekipy w terenie', icon: 'mdi-account-group', value: 6, color: 'success' },
  { label: 'Klienci', icon: 'mdi-account-tie', value: 27, color: 'info' },
  { label: 'Zgłoszenia', icon: 'mdi-alert-octagon', value: 3, color: 'error' },
]
</script>

<template>
  <v-row class="mb-3">
    <v-col v-for="kpi in kpis" :key="kpi.label" cols="12" sm="6" md="3">
      <v-card :color="kpi.color" class="d-flex align-center pa-4" elevation="2">
        <v-icon size="36" class="me-3 white--text">{{ kpi.icon }}</v-icon>
        <div>
          <div class="text-h5 white--text">{{ kpi.value }}</div>
          <div class="text-caption white--text">{{ kpi.label }}</div>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>
