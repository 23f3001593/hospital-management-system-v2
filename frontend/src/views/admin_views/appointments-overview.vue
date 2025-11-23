<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <AppointmentsTable :past="false" title="Scheduled Appointments" :appointments="scheduledAppointments"/>
        <AppointmentsTable :past="true" title="Past Appointments" :appointments="pastAppointments"/>
    </div>
</template>

<script>
    import axios from "axios";
    import AppointmentsTable from "@/components/admin_components/appointments-table.vue";
    export default {
        name: "AppointmentsOverview",
        components: { AppointmentsTable },
        data() {
            return {
                scheduledAppointments: [],
                pastAppointments: [],
                loading: false,
            };
        },
        methods: {
            async fetchAppointments() {
                this.loading = true;
                const res = await axios.get("/admin/appointments");
                this.scheduledAppointments = res.data.scheduled_appointments || [];
                this.pastAppointments = res.data.past_appointments || [];
                this.loading = false;
            },
        },
        mounted() {
            this.fetchAppointments();
        },
    };
</script>