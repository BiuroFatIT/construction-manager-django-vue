<script setup lang="ts">
import DashboardKPIs from "../components/DashboardKPIs.vue";
import DashboardProjectsChart from "../components/DashboardProjectsChart.vue";
import DashboardTeamsChart from "../components/DashboardTeamsChart.vue";
import DashboardCalendarWidget from "../components/DashboardCalendarWidget.vue";
import GanntChart from "../components/GanntChart.vue";
</script>

<template>

  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4" color="blue-grey-darken-4" variant="elevated">
          <v-card-title class="white--text text-h5">
            <v-icon class="me-2">mdi-view-dashboard-outline</v-icon>
            Construction Manager – Dashboard
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <!-- KPI quick stats -->
      <v-col cols="12">
        <DashboardKPIs />
      </v-col>
      <!-- Gantt chart -->
      <v-col cols="12">
        <GanntChart />
      </v-col>
    </v-row>
    <v-row>
      <!-- Wykres projektów po etapach i statusach -->
      <v-col cols="12" md="7">
        <DashboardProjectsChart />
      </v-col>
      <!-- Wykres aktywności ekip -->
      <v-col cols="12" md="5">
        <DashboardTeamsChart />
      </v-col>
    </v-row>
    <v-row>
      <!-- Widget kalendarzowy np. na dziś/jutro/tydzień -->
      <v-col cols="12" md="6">
        <DashboardCalendarWidget />
      </v-col>
      <!-- Możesz dorzucić np. listę ostatnich zgłoszeń, klientów, przypomnień -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>
            <v-icon class="me-2">mdi-account-group</v-icon>
            Ostatnie zgłoszenia ekip
          </v-card-title>
          <v-card-text>
            <v-list density="compact">
              <v-list-item v-for="item in 3" :key="item">
                <v-list-item-title>
                  Ekipa #{{ item }}: Zgłoszono awarię dźwigu na budowie A{{
                    item
                  }}
                </v-list-item-title>
                <v-list-item-subtitle>2 godziny temu</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
