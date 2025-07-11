<script setup lang="ts">
const events = [
  { time: '08:00', label: 'Rozpoczęcie prac – Projekt A' },
  { time: '10:30', label: 'Spotkanie z klientem – Budowa B' },
  { time: '14:00', label: 'Dostawa materiałów – Magazyn' },
]
</script>

<template>
  <v-card class="mb-4">
    <v-card-title>
      <v-icon class="me-2">mdi-calendar</v-icon>
      Kalendarz – Dzisiaj
    </v-card-title>
    <v-card-text>
      <v-timeline align="start" dense>
        <v-timeline-item
          v-for="(ev, i) in events"
          :key="i"
          dot-color="primary"
        >
          <strong>{{ ev.time }}</strong> — {{ ev.label }}
        </v-timeline-item>
      </v-timeline>
    </v-card-text>
  </v-card>
</template>
