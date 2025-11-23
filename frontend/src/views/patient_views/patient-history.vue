<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <AppointmentsTablePatient :past="true" title="Appointments History" :appointments="appointments"/>
    </div>
</template>

<script>
    import axios from "axios";
    import AppointmentsTablePatient from "@/components/patient_components/appointments-table-patient.vue";
    export default {
        name: "PatientHistory",
        components: { AppointmentsTablePatient },
        data() {
            return {
                appointments: [],
                loading: false,
            };
        },
        methods: {
            async fetchAppointments() {
                this.loading = true;
                const id = this.$store.state.user.id;
                const response = await axios.get(`/patient/appointments/past/${id}`);
                this.appointments = response.data.appointments || [];
                this.appointments.sort((a, b) => {
                    const dateA = new Date(a.appointment_date);
                    const dateB = new Date(b.appointment_date);
                    if (dateA > dateB) return -1;
                    if (dateA < dateB) return 1;
                    const timeA = a.slot?.slot_time || "";
                    const timeB = b.slot?.slot_time || "";
                    return timeB.localeCompare(timeA);
                });
                this.loading = false;
            },
        },
        mounted() {
            this.fetchAppointments();
        },
    };
</script>