<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <AppointmentsTablePatient title="Scheduled Appointments" :appointments="appointments" @appointmentsChanged="fetchData"/>
        <DepartmentsGridPatient title="Departments" :departments="departments"/>
    </div>
</template>

<script>
    import axios from "axios";
    import AppointmentsTablePatient from "@/components/patient_components/appointments-table-patient.vue";
    import DepartmentsGridPatient from "@/components/patient_components/departments-grid-patient.vue";
    export default {
        name: "PatientHome",
        components: { DepartmentsGridPatient, AppointmentsTablePatient },
        data() {
            return {
                appointments: [],
                departments: [],
                loading: false,
            };
        },
        methods: {
            async fetchData() {
                this.loading = true;
                const id = this.$store.state.user.id;
                const res1 = await axios.get(`/patient/appointments/${id}`);
                this.appointments = res1.data.appointments || [];
                this.appointments.sort((a, b) => {
                    const dateA = new Date(a.appointment_date);
                    const dateB = new Date(b.appointment_date);
                    if (dateA < dateB) return -1;
                    if (dateA > dateB) return 1;
                    const timeA = a.slot?.slot_time || "";
                    const timeB = b.slot?.slot_time || "";
                    return timeA.localeCompare(timeB);
                });
                const res2 = await axios.get("/admin/departments");
                this.departments = res2.data.departments || [];
                this.loading = false;
            },
        },
        mounted() {
            this.fetchData();
        },
    };
</script>