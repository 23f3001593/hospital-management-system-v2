import Home from "@/views/main_views/home.vue";
import HomePage from "@/views/main_views/home-page.vue";
import Login from "@/views/main_views/login.vue";
import CreatePatient from "@/views/patient_views/create-patient.vue";

export default [{
    path: "/",
    component: Home,
    meta: { requiresAuth: false },
    children: [
        { path: "", component: HomePage },
        { path: "login", component: Login },
        { path: "register", component: CreatePatient },
    ],
}];