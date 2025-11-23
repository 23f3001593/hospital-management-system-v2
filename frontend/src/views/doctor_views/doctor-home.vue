<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <AppointmentsTableDoctor :past="false" :today="true" title="Scheduled Appointments for Today" :appointments="today_appointments" @appointmentsChanged="fetchAppointments"/>
        <AppointmentsTableDoctor :past="false" :today="false" title="Scheduled Appointments for Week" :appointments="week_appointments" @appointmentsChanged="fetchAppointments"/>
    </div>
</template>

<script>
    import axios from "axios";
    import AppointmentsTableDoctor from "@/components/doctor_components/appointments-table-doctor.vue";
    export default {
        name: "DoctorHome",
        components: { AppointmentsTableDoctor },
        data() {
            return {
                today_appointments: [],
                week_appointments: [],
                loading: false,
            };
        },
        methods: {
            async fetchAppointments() {
                this.loading = true;
                const id = this.$store.state.user.id;
                const response = await axios.get(`/doctor/appointments/scheduled/${id}`);
                const appointments = response.data.appointments || [];
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                this.today_appointments = appointments
                .filter(appt => {
                    const d = new Date(appt.appointment_date);
                    return d.toDateString() === today.toDateString();
                })
                .sort((a, b) => {
                    const dateA = new Date(a.appointment_date);
                    const dateB = new Date(b.appointment_date);
                    if (dateA < dateB) return -1;
                    if (dateA > dateB) return 1;
                    const timeA = a.slot?.slot_time || "";
                    const timeB = b.slot?.slot_time || "";
                    return timeA.localeCompare(timeB);
                });
                const dayOfWeek = today.getDay(); 
                const daysUntilSunday = (7 - dayOfWeek) % 7; 
                let endOfWeek = new Date(today);
                endOfWeek.setDate(today.getDate() + daysUntilSunday);
                endOfWeek.setHours(23, 59, 59, 999);
                const startOfRange = new Date(today);
                startOfRange.setDate(today.getDate() + 1);
                startOfRange.setHours(0, 0, 0, 0);
                this.week_appointments = appointments
                .filter(appt => {
                    const d = new Date(appt.appointment_date);
                    return d >= startOfRange && d <= endOfWeek;
                })
                .sort((a, b) => {
                    const dateA = new Date(a.appointment_date);
                    const dateB = new Date(b.appointment_date);
                    if (dateA < dateB) return -1;
                    if (dateA > dateB) return 1;
                    const timeA = a.slot?.slot_time || "";
                    const timeB = b.slot?.slot_time || "";
                    return timeA.localeCompare(timeB);
                });
                this.loading = false;
            },
        },
        mounted() {
            this.fetchAppointments();
        },
    };
</script>