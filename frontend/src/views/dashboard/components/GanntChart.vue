<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Gantt from 'frappe-gantt'
import '@/assets/frappe-gannt/frappe-gantt.css'

// Ref do HTML-a musi mieć typ
const chartRef = ref<HTMLElement | null>(null)
// Typuj ref gantta (jak nie ma type, daj any)
const ganttInstance = ref<any>(null) // lub ref<GanttType | null>(null) jeśli masz typings

const tasks = [
  {
    id: '1',
    name: 'Przygotowanie dokumentacji',
    start: '2025-07-01',
    end: '2025-07-05',
    progress: 30,
    custom_class: 'bar-blue'
  },
  {
    id: '2',
    name: 'Budowa fundamentów',
    start: '2025-07-06',
    end: '2025-07-15',
    progress: 10,
    dependencies: '1',
    custom_class: 'bar-green'
  },
  {
    id: '3',
    name: 'Montaż instalacji',
    start: '2025-07-16',
    end: '2025-07-20',
    progress: 0,
    dependencies: '2'
  }
]

onMounted(() => {
  if (chartRef.value) {
    ganttInstance.value = new Gantt(chartRef.value, tasks, {
      view_mode: 'Day',
      language: 'pl',
      today_button: true
    })
  }
})
</script>

<template>
  <div>
    <v-card class="mb-4">
      <v-card-title>
        <v-icon class="me-2">mdi-timeline</v-icon>
        Gantt – Harmonogram projektu
      </v-card-title>
      <v-card-text>
        <div ref="chartRef" style="overflow-x:auto; min-height:50vh;"></div>
      </v-card-text>
    </v-card>
  </div>
</template>

<style scoped>
.bar-blue .bar {
  fill: #1976d2 !important;
}
.bar-green .bar {
  fill: #43a047 !important;
}
.gantt-card {
  height: 85vh;
  display: flex;
  flex-direction: column;
}
.gantt-content {
  flex: 1 1 auto;
  overflow: auto;
  padding: 0;
}
.gantt-chart {
  height: 100%;
  min-height: 500px;
  width: 100%;
}
</style>
