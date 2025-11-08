import Login from "@/views/main_views/login.vue";
import CreatePatient from "@/views/patient_views/create-patient.vue";

export default [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/register", component: CreatePatient },
];