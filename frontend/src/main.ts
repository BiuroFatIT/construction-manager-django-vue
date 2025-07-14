// Plugins
import vuetify from "../src/plugins/vuetify";
import { createI18n } from "vue-i18n";

// Components
import App from "./App.vue";

// Messages
import messages from "./i18n/index";

// Composables
import { createApp } from "vue";
import { createPinia } from "pinia";
import router from "./router";

const i18n = createI18n({
    legacy: false,
    locale: 'pl',
    fallbackLocale: 'en',
    messages
  })
  
const app = createApp(App);

app.use(i18n);
app.use(createPinia());
app.use(vuetify);
app.use(router);
app.mount("#app");
