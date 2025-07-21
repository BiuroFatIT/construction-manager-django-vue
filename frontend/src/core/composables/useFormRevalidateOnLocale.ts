// useFormRevalidateOnLocale.ts

import { watch, nextTick } from 'vue'
import { useI18n } from "vue-i18n";
import { useLanguageStore } from '@/stores/language';

export function useFormRevalidateOnLocale(formRef: any) {
  const languageStore = useLanguageStore();
  const { locale } = useI18n();
  watch(
    () => languageStore.selected,
    (newLocale) => {
      locale.value = newLocale;
    },
    { immediate: true }
  );

  watch(
    () => locale.value,
    async () => {
      await nextTick();
      formRef.value?.resetValidation();
      await nextTick();
      formRef.value?.validate();
    }
  );
}
