<script setup lang="ts">
import { ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useLanguageStore } from "../stores/language";

const languages = [
  { code: "pl", label: "Polski", icon: "mdi-flag" },
  { code: "en", label: "English", icon: "mdi-flag-outline" },
];

const menu = ref(false);
const languageStore = useLanguageStore();
const { locale, t } = useI18n();

locale.value = languageStore.selected;

watch(
  () => languageStore.selected,
  (lang) => {
    locale.value = lang;
  }
);

function selectLanguage(lang: string) {
  languageStore.setLanguage(lang);
  menu.value = false;
}
</script>

<template>
  <v-tooltip :text="t('language_switcher.title')">
    <template #activator="{ props: tooltipProps }">
      <v-menu v-model="menu" location="bottom">
        <template #activator="{ props: menuProps }">
          <v-btn
            icon
            v-bind="{ ...tooltipProps, ...menuProps }"
            variant="plain"
            :aria-label="t('language_switcher.title')"
          >
            <v-icon>mdi-earth</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="lang in languages"
            :key="lang.code"
            @click="selectLanguage(lang.code)"
            :active="languageStore.selected === lang.code"
          >
            <v-list-item-title>
              <v-icon start size="small">{{ lang.icon }}</v-icon>
              {{ lang.label }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
  </v-tooltip>
</template>
