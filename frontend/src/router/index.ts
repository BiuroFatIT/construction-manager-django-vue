import type { RouteRecordRaw } from "vue-router";

import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

import LoginView from "@/views/login/containers/LoginView.vue";
import DashboardView from "@/views/dashboard/containers/DashboardView.vue";
import CompanyView from "@/views/company/containers/CompanyView.vue";
import TeamsView from "@/views/teams/containers/TeamsView.vue";



const routes: Array<RouteRecordRaw> = [
  {
    path: "/login",
    component: LoginView,
    name: "Login",
    meta: { title: "Logowanie" },
  },
  {
    path: "/",
    name: "Home",
    component: DashboardView,
    meta: { requiresAuth: true, title: "Strona główna" },
  },
  {
    path: "/company/list",
    name: "CompanyList",
    component: CompanyView,
    meta: { requiresAuth: true, title: "Company List" },
  },
  {
    path: "/teams/list",
    name: "TeamsList",
    component: TeamsView,
    meta: { requiresAuth: true, title: "Teams List" },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.onError((err, to) => {
  if (err?.message?.includes?.("Failed to fetch dynamically imported module")) {
    if (localStorage.getItem("vuetify:dynamic-reload")) {
      console.error("Dynamic import error, reloading page did not fix it", err);
    } else {
      console.log("Reloading page to fix dynamic import error");
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

// Obsługa auth i title
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  if (!auth.isAuthReady) {
    await auth.initialize()
  }
  if (to.path === "/login" && auth.isLoggedIn) {
    next("/")
    return
  }
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    next({ path: "/login", query: { next: to.fullPath } })
    return
  }
  next()
})


router.afterEach((to) => {
  document.title = (to.meta.title as string) || "Construction Manager"
})

export default router;
