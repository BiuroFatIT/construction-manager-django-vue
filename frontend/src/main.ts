// Plugins
import { createI18n } from "vue-i18n";
import { definePreset } from '@primeuix/themes';
import ToastService from 'primevue/toastservice';
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import 'primeicons/primeicons.css';
// Components
import App from "./App.vue";

// Messages
import messages from "./i18n/index";

// Composables
import { createApp } from "vue";
import { createPinia } from "pinia";
import router from "./router";

// Styles

import "./assets/main.css";

const i18n = createI18n({
    legacy: false,
    locale: 'pl',
    fallbackLocale: 'en',
    messages
  })
  
const app = createApp(App);

app.use(i18n);
app.use(createPinia());
app.use(router);
app.use(PrimeVue, {
  // Default theme configuration
  theme: {
      preset: Aura,
      options: {
          prefix: 'p',
          darkModeSelector: false,
          cssLayer: false
      }
  }
}).use(ToastService);
app.mount("#app");
