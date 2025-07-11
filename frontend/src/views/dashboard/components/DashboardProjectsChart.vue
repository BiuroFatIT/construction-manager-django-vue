<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'

Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const chartData = ref({
  labels: ['W realizacji', 'Zakończone', 'Wstrzymane'],
  datasets: [
    {
      label: 'Projekty',
      data: [6, 5, 3],
      backgroundColor: ['#1976d2', '#388e3c', '#f44336'],
    }
  ]
})

const chartOptions = ref({
  responsive: true,
  plugins: { legend: { display: false } }
})
</script>

<template>
  <v-card class="mb-4">
    <v-card-title>
      <v-icon class="me-2">mdi-chart-bar</v-icon>
      Projekty wg statusu
    </v-card-title>
    <v-card-text>
      <Bar :data="chartData" :options="chartOptions" />
    </v-card-text>
  </v-card>
</template>
