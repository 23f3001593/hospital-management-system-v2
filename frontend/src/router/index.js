import { createRouter, createWebHistory } from 'vue-router'
import store from "@/store"
import Login from "@/views/main_views/login.vue";
import RegisterPatient from "@/views/patient_views/register-patient.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/patient/register", component: RegisterPatient }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.isAuthenticated

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login")
  } else if (to.path === "/login" && isAuthenticated) {
    // next("/dashboard")
    next("/login")
  } else {
    next()
  }
})

export default router