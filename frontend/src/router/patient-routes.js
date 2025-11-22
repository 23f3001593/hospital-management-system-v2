import PatientDashboard from "@/views/patient_views/patient-dashboard.vue";
import PatientHome from "@/views/patient_views/patient-home.vue";
import DepartmentOverview from "@/views/patient_views/department-overview.vue";
import TreatmentsOverview from "@/views/patient_views/treatments-overview.vue";
import UpdatePatient from "@/views/patient_views/update-patient.vue";

export default [{
    path: "/patient",
    component: PatientDashboard,
    meta: { requiresAuth: true },
    children: [
        { path: "", component: PatientHome },
        { path: "department/:id", component: DepartmentOverview, name: 'DepartmentOverview'},
        { path: "treatments", component: TreatmentsOverview },
        { path: "account", component: UpdatePatient },
    ],
}];