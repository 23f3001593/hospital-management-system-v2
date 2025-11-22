import DoctorDashboard from "@/views/doctor_views/doctor-dashboard.vue";
import DoctorHome from "@/views/doctor_views/doctor-home.vue";
import Availability from "@/views/doctor_views/availability.vue";
import UpdateDoctor from "@/views/doctor_views/update-doctor.vue";

export default [{
    path: "/doctor",
    component: DoctorDashboard,
    meta: { requiresAuth: true },
    children: [
        { path: "", component: DoctorHome },
        { path: "availability", component: Availability },
        { path: "account", component: UpdateDoctor },
    ],
}];