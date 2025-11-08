import { createRouter, createWebHistory } from 'vue-router'
import store from "@/store"

import mainRoutes from "@/router/main-routes";
import adminRoutes from "@/router/admin-routes";

const routes = [
  ...mainRoutes,
  ...adminRoutes,
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.isAuthenticated
  const role = store.state.user.role

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login")
  } else if (to.path === "/login" && isAuthenticated) {
    if (role === "admin") {
      next("/admin")
    } else if (role === "doctor") {
      next("/doctor")
    } else if (role === "patient") {
      next("/patient")
    } else {
      next("/")
    }
  } else if (to.path.startsWith("/admin") && role !== "admin") {
    next("/")
  } else if (to.path.startsWith("/doctor") && role !== "doctor") {
    next("/")
  } else if (to.path.startsWith("/patient") && role !== "patient") {
    next("/")
  } else {
    next()
  }
})
router.afterEach(() => {
  document.body.style.overflow = "";
  document.body.style.paddingRight = "";
});

export default router