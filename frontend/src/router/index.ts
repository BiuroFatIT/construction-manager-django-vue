/// <reference types="vite/client" />

import type { RouteRecordRaw } from "vue-router";
import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    component: () => import("@/layout/AppLayout.vue"),
    children: [
      {
        path: "",
        name: "dashboard",
        component: () => import("@/views/dashboard/containers/DashboardView.vue"),
        meta: { requiresAuth: true, title: "Strona główna" },
      },
      {
        path: "cm",
        name: "constructionManager",
        meta: { requiresAuth: true, title: "Construction Manager" },
        children: [
          {
            path: "companies",
            name: "cm-companies",
            component: () => import("@/views/companies/containers/CompaniesView.vue"),
            meta: { requiresAuth: true, title: "Companies" },
          },
          {
            path: "products",
            name: "cm-products",
            component: () => import("@/views/products/containers/ProductsView.vue"),
            meta: { requiresAuth: true, title: "Products" },
          },
          {
            path: "users",
            name: "cm-users",
            component: () => import("@/views/users/containers/UsersView.vue"),
            meta: { requiresAuth: true, title: "Users" },
          },
        ],
      },
    ],
  },
  {
    path: "/auth/login",
    name: "login",
    component: () => import("@/views/login/containers/LoginView.vue"),
    meta: { title: "Logowanie" },
  },
  {
    path: "/auth/access",
    name: "accessDenied",
    component: () => import("@/views/general/AuthAccessDenied.vue"),
    meta: { title: "Brak dostępu" },
  },
  {
    path: "/auth/error",
    name: "error",
    component: () => import("@/views/general/AuthError.vue"),
    meta: { title: "Błąd uwierzytelniania" },
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: { name: "notfound" },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// recovery dla błędów dynamicznych importów
router.onError((err, to) => {
  if (err?.message?.includes?.("Failed to fetch dynamically imported module")) {
    if (localStorage.getItem("vuetify:dynamic-reload")) {
      console.error("Dynamic import error, reload nie pomógł", err);
    } else {
      console.log("Przeładowanie strony w celu naprawy dynamic import error");
      localStorage.setItem("vuetify:dynamic-reload", "true");
      location.assign(to.fullPath);
    }
  } else {
    console.error(err);
  }
});

router.isReady().then(() => {
  localStorage.removeItem("vuetify:dynamic-reload");
});

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();
  if (!auth.isAuthReady) {
    await auth.initialize();
  }

  // jeśli jesteśmy na loginie i już zalogowany → dashboard
  if ((to.name === "login" || to.path === "/login") && auth.isLoggedIn) {
    next({ name: "dashboard" });
    return;
  }

  // ochrona tras wymagających uwierzytelnienia
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    next({
      path: "/auth/login",
      query: { next: to.fullPath },
    });
    return;
  }

  next();
});

router.afterEach((to) => {
  const defaultTitle = "Construction Manager";
  document.title = (to.meta.title as string) || defaultTitle;
});

export default router;
