import { createApp } from 'vue';
import { createI18n } from "vue-i18n";
import App from './App.vue';
import router from './router';

import Aura from '@primevue/themes/aura';
import PrimeVue from 'primevue/config';
import StyleClass from 'primevue/styleclass';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import DialogService from 'primevue/dialogservice'
import DynamicDialog from 'primevue/dynamicdialog'
import { createPinia } from "pinia";

// Styles
import '@/assets/styles.scss';
import '@/assets/tailwind.css';

// Messages
import messages from "./i18n/index";


const app = createApp(App);

const i18n = createI18n({
    legacy: false,
    locale: 'pl',
    fallbackLocale: 'en',
    messages
  })

app.use(i18n);
app.use(createPinia());
app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.app-dark'
        }
    }
});
app.directive('styleclass', StyleClass);
app.use(ToastService);
app.use(ConfirmationService);
app.use(DialogService)

app.component('DynamicDialog', DynamicDialog)

app.mount('#app');
