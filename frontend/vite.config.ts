import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import Layouts from "vite-plugin-vue-layouts-next";
import vue from "@vitejs/plugin-vue";
import VueRouter from "unplugin-vue-router/vite";
import tailwindcss from "@tailwindcss/vite";
import { PrimeVueResolver } from "unplugin-vue-components/resolvers";
import { VueRouterAutoImports } from "unplugin-vue-router";
import { defineConfig } from "vite";
import { fileURLToPath, URL } from "node:url";

const DEV_BASE = "/";
const PROD_BASE = "/static/";

export default defineConfig(({ mode }) => {
  const isProd = mode === "production";

  return {
    plugins: [
      VueRouter({
        dts: "src/typed-router.d.ts",
      }),
      Layouts(),
      tailwindcss(),
      AutoImport({
        imports: [
          "vue",
          VueRouterAutoImports,
          {
            pinia: ["defineStore", "storeToRefs"],
          },
        ],
        dts: "src/auto-imports.d.ts",
        eslintrc: {
          enabled: true,
        },
        vueTemplate: true,
      }),
      Components({
        resolvers: [PrimeVueResolver()],
        dts: "src/components.d.ts",
      }),
      vue({}),
    ],
    base: isProd ? PROD_BASE : DEV_BASE,
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("src", import.meta.url)),
      },
      extensions: [".js", ".json", ".jsx", ".mjs", ".ts", ".tsx", ".vue"],
    },
    server: {
      host: "localhost",
      port: 5173,
      open: true,
      hmr: true,
      proxy: {
        "/api": "http://localhost:8000",
      },
    },
    optimizeDeps: {
      exclude: [
        "vue-router",
        "unplugin-vue-router/runtime",
        "unplugin-vue-router/data-loaders",
        "unplugin-vue-router/data-loaders/basic",
      ],
    },
    define: { "process.env": {} },
    build: {
      sourcemap: !isProd,
    },
  };
});
