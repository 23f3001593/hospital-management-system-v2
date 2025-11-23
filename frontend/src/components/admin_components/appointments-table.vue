<template>
    <div class="container my-5">
        <div class="d-flex align-items-center justify-content-between mb-4">
            <h2 class="mb-0 fw-bold">{{ title }}</h2>
            <div class="input-group search-bar">
                <span class="input-group-text"><i class="bi bi-search"></i></span>
                <input type="text" v-model="searchQuery" class="form-control" placeholder="Type to search..."/>
            </div>
        </div>
        <div class="card">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-striped table-hover mb-0 text-center align-middle">
                        <thead>
                            <tr>
                                <th scope="col">ID</th>
                                <th scope="col">Department</th>
                                <th scope="col">Doctor</th>
                                <th scope="col">Patient</th>
                                <th scope="col">Date</th>
                                <th scope="col">Time</th>
                                <th v-if="past" scope="col">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="appointment in filteredAppointments" :key="appointment.appointment_id">
                                <td>{{ appointment.appointment_id }}</td>
                                <td>{{ appointment.doctor.department.department_name }}</td>
                                <td>{{ appointment.doctor.user.username }}</td>
                                <td>{{ appointment.patient.user.username }}</td>
                                <td>{{ formatDate(appointment.appointment_date) }}</td>
                                <td>{{ formatTime(appointment.slot.slot_time) }}</td>
                                <td v-if="past" :class="{'text-success': appointment.status === 'completed','text-danger': appointment.status === 'cancelled'}">{{ formatStatus(appointment.status) }}</td>
                            </tr>
                            <tr v-if="appointments.length > 0 && filteredAppointments.length === 0">
                                <td v-bind:colspan="past ? 7 : 6" class="text-muted fst-italic">
                                    No matching records found.
                                </td>
                            </tr>
                            <tr v-if="appointments.length === 0">
                                <td v-bind:colspan="past ? 7 : 6" class="text-muted fst-italic">No appointments found.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "AppointmentsTable",
        props: {
            title: String,
            appointments: Array,
            past: Boolean,
        },
        data() {
            return {
                searchQuery: "",
            };
        },
        computed: {
            filteredAppointments() {
                if (!this.searchQuery.trim()) return this.appointments;
                const q = this.searchQuery.toLowerCase();
                return this.appointments.filter((appointment) => {
                    return (
                        String(appointment.appointment_id).includes(q) ||
                        appointment.doctor.department.department_name.toLowerCase().includes(q) ||
                        appointment.doctor.user.username.toLowerCase().includes(q) ||
                        appointment.patient.user.username.toLowerCase().includes(q) ||
                        this.formatDate(appointment.appointment_date).toLowerCase().includes(q) ||
                        this.formatTime(appointment.slot.slot_time).toLowerCase().includes(q) ||
                        (this.past && appointment.status.toLowerCase().includes(q))
                    );
                });
            },
        },
        methods: {
            formatDate(appointment_date) {
                if (!appointment_date) return "";
                const date = new Date(appointment_date);
                const options = { day: '2-digit', month: 'short', year: 'numeric' };
                return date.toLocaleDateString('en-GB', options);
            },
            formatHour(hour, minute) {
                const suffix = hour >= 12 ? "pm" : "am";
                const normalizedHour = hour % 12 || 12;
                const paddedHour = normalizedHour.toString().padStart(2, "0");
                const paddedMinute = minute.toString().padStart(2, "0");
                return `${paddedHour}:${paddedMinute}${suffix}`;
            },
            formatTime(slot_time) {
                if (!slot_time) return "";
                let [hour, minute] = slot_time.split(":").map(Number);
                const start = this.formatHour(hour, minute);
                let endHour = hour + 1;
                if (endHour === 24) endHour = 0;
                const end = this.formatHour(endHour, minute);
                return `${start} - ${end}`;
            },
            formatStatus(status) {
                return status.charAt(0).toUpperCase() + status.slice(1);
            },
        },
    };
</script>

<style scoped>
    .search-bar {
        width: 100%;
        max-width: 300px;
    }
    .input-group .form-control{
        outline: none !important;
        box-shadow: none !important;
    }
</style>