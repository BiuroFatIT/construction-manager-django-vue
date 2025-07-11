/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

// Composables
import { createVuetify } from "vuetify";

const savedTheme = localStorage.getItem("theme");

// 2. Ustalamy, który motyw będzie domyślny przy starcie aplikacji
const defaultTheme =
  savedTheme === "dark"
    ? "dark"
    : savedTheme === "grey-orange"
    ? "grey-orange"
    : savedTheme === "violet"
    ? "violet"
    : "light";

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    // 4. Włączamy domyślny motyw
    defaultTheme,
    themes: {
      // 5. Standardowy jasny motyw (tu wpisz swoje kolory)
      light: {
        /* … */
      },
      // 6. Standardowy ciemny motyw (tu wpisz swoje kolory)
      dark: {
        /* … */
      },
      // 7. Szaro-pomarańczowy motyw
      "grey-orange": {
        // czy ten motyw traktować jak dark mode (inwersja ikon itp.)
        dark: false,
        colors: {
          // a) tło aplikacji (<body>, kontenery root)
          background: "#f4f4f5",
          // b) powierzchnie komponentów (karty, dialogi, listy)
          surface: "#ffffff",
          // c) główny kolor akcentu (np. color="primary" na przyciskach)
          primary: "#ff9800",
          // d) ciemniejsza wersja primary (np. hover/active)
          "primary-darken-1": "#ff8200",
          // e) drugi akcent o mniejszym natężeniu
          secondary: "#757575",
          // f) ciemniejszy odcień secondary
          "secondary-darken-1": "#616161",
          // g) dodatkowy kontrastowy akcent (color="accent")
          accent: "#ffb74d",
          // h) kolor stanów błędu (v-messages, error badges)
          error: "#ef5350",
          // i) kolor informacji (info alerts)
          info: "#42a5f5",
          // j) kolor powodzenia (success alerts)
          success: "#66bb6a",
          // k) kolor ostrzeżeń (warning badges)
          warning: "#ffa726",
          // l) bazowa neutralna szarość do dividerów, tła itp.
          grey: "#bdbdbd",
          // m) ciemniejsza szarość
          "grey-darken-1": "#757575",
          // n) jaśniejsza szarość
          "grey-lighten-1": "#e0e0e0",
          // o) domyślny kolor tekstu/ikon na background
          "on-background": "#23272a",
          // p) domyślny kolor tekstu/ikon na surface
          "on-surface": "#23272a",
          // q) domyślny kolor tekstu/ikon na primary
          "on-primary": "#ffffff",
          // r) domyślny kolor tekstu/ikon na secondary
          "on-secondary": "#ffffff",
          // s) domyślny kolor tekstu/ikon na accent
          "on-accent": "#ffffff",
        },
      },
      // 8. Nowy, fioletowy motyw
      violet: {
        // czy to dark mode?
        dark: false,
        colors: {
          // a) tło aplikacji
          background: "#f3e5f5",
          // b) powierzchnie komponentów
          surface: "#ffffff",
          // c) główny akcent (primary)
          primary: "#9c27b0",
          // d) ciemniejszy primary (hover/active)
          "primary-darken-1": "#8e24aa",
          // e) secondary akcent
          secondary: "#7b1fa2",
          // f) ciemniejszy secondary
          "secondary-darken-1": "#6a1b9a",
          // g) dodatkowy accent
          accent: "#e1bee7",
          // h) error
          error: "#e040fb",
          // i) info
          info: "#ab47bc",
          // j) success
          success: "#ba68c8",
          // k) warning
          warning: "#ce93d8",
          // l) neutralna grey
          grey: "#bdbdbd",
          // m) ciemniejsza grey
          "grey-darken-1": "#757575",
          // n) jaśniejsza grey
          "grey-lighten-1": "#e0e0e0",
          // o) tekst/ikony na background
          "on-background": "#212121",
          // p) tekst/ikony na surface
          "on-surface": "#212121",
          // q) tekst/ikony na primary
          "on-primary": "#ffffff",
          // r) tekst/ikony na secondary
          "on-secondary": "#ffffff",
          // s) tekst/ikony na accent
          "on-accent": "#ffffff",
        },
      },
    },
  },
});
