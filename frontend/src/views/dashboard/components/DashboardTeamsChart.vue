<script setup lang="ts">
import { ref } from 'vue'
import { Pie } from 'vue-chartjs'
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js'
Chart.register(ArcElement, Tooltip, Legend)

const data = ref({
  labels: ['Ekipa A', 'Ekipa B', 'Ekipa C', 'Ekipa D'],
  datasets: [{
    data: [3, 2, 1, 4],
    backgroundColor: ['#1e88e5', '#43a047', '#ffa726', '#d32f2f'],
  }]
})
</script>

<template>
  <v-card class="mb-4">
    <v-card-title>
      <v-icon class="me-2">mdi-chart-pie</v-icon>
      Aktywność ekip
    </v-card-title>
    <v-card-text>
      <Pie :data="data" />
    </v-card-text>
  </v-card>
</template>
