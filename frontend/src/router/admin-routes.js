import AdminDashboard from "@/views/admin_views/admin-dashboard.vue";
import AdminHome from "@/views/admin_views/admin-home.vue";
import DepartmentsOverview from "@/views/admin_views/departments-overview.vue";
import DoctorsOverview from "@/views/admin_views/doctors-overview.vue";
import CreateDoctor from "@/views/admin_views/create-doctor.vue";
import PatientsOverview from "@/views/admin_views/patients-overview.vue";
import AppointmentsOverview from "@/views/admin_views/appointments-overview.vue";
import UpdateAdmin from "@/views/admin_views/update-admin.vue";

export default [{
    path: "/admin",
    component: AdminDashboard,
    meta: { requiresAuth: true },
    children: [
        { path: "", component: AdminHome },
        { path: "departments", component: DepartmentsOverview },
        { path: "doctors", component: DoctorsOverview },
        { path: "doctor/create", component: CreateDoctor },
        { path: "patients", component: PatientsOverview },
        { path: "appointments", component: AppointmentsOverview },
        { path: "account", component: UpdateAdmin },
    ],
}];