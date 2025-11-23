<template>
    <div class="container my-5">
        <div class="d-flex align-items-center justify-content-between mb-4">
            <h2 class="mb-0 fw-bold">{{ title }}</h2>
            <div v-if="past" class="input-group search-bar">
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
                                <th scope="col">S/N</th>
                                <th scope="col">Department</th>
                                <th scope="col">Doctor</th>
                                <th scope="col">Date</th>
                                <th v-if="!past" scope="col">Day</th>
                                <th scope="col">Time</th>
                                <th v-if="past" scope="col">Fees</th>
                                <th v-if="past" scope="col">Status</th>
                                <th v-if="!past" scope="col">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(appointment,index) in filteredAppointments" :key="appointment.appointment_id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ appointment.doctor.department.department_name }}</td>
                                <td>{{ appointment.doctor.user.full_name }}</td>
                                <td>{{ formatDate(appointment.appointment_date) }}</td>
                                <td v-if="!past">{{ formatDay(appointment.appointment_date) }}</td>
                                <td>{{ formatTime(appointment.slot.slot_time) }}</td>
                                <td v-if="past">{{ formatFees(appointment.doctor.fees) }}</td>
                                <td v-if="past" :class="{'text-success': appointment.status === 'completed','text-danger': appointment.status === 'cancelled'}">{{ formatStatus(appointment.status) }}</td>
                                <td v-if="!past">
                                    <button type="button" class="btn btn-sm btn-primary position-relative me-2" :disabled="rowLoading[appointment.appointment_id]" @click="openRescheduleAppointmentModal(appointment)">
                                        <span class="d-inline-block text-center w-100" :class="{ 'invisible': rowLoading[appointment.appointment_id] }">Reschedule</span>
                                        <div v-show="rowLoading[appointment.appointment_id]" class="position-absolute top-50 start-50 translate-middle">
                                            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                        </div>
                                    </button>
                                    <button type="button" class="btn btn-sm btn-danger" @click="openCancelAppointmentModal(appointment)">Cancel</button>
                                </td>
                            </tr>
                            <tr v-if="past && appointments.length > 0 && filteredAppointments.length === 0">
                                <td colspan="7" class="text-muted fst-italic">
                                    No matching records found.
                                </td>
                            </tr>
                            <tr v-if="appointments.length === 0">
                                <td colspan="7" class="text-muted fst-italic">No appointments found.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div v-if="showRescheduleAppointmentModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-xl modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary d-flex justify-content-center align-items-center">
                        <h2 class="text-center mb-0 fw-bold">Reschedule Appointment</h2>
                    </div>
                    <div class="modal-body">
                        <div class="card">
                            <div class="card-body p-0">
                                <div class="table-responsive">
                                    <table class="table table-striped mb-0 text-center align-middle">
                                        <thead>
                                            <tr>
                                                <th scope="col">Day</th>
                                                <th scope="col">Date</th>
                                                <th scope="col">Availability</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(day, index) in orderedDays" :key="day">
                                                <td>{{ day }}</td>
                                                <td>{{ getDateForDay(index) }}</td>
                                                <td>
                                                    <div class="d-flex flex-wrap justify-content-center gap-2">
                                                        <button
                                                            v-for="(slot, i) in 6"
                                                            :key="i"
                                                            class="btn btn-sm fw-semibold"
                                                            :class="buttonClass(day, i, isSlotDisabled(day, i))"
                                                            :style="isSlotDisabled(day, i) ? 'pointer-events:none; opacity:1;' : (!editableSlot[day]?.[i] ? 'pointer-events:none; opacity:1;' : '')"
                                                            @click="selectSlot(day, i)"
                                                        >
                                                            {{ slotLabels[i] }}
                                                        </button>
                                                    </div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <div class="w-100">
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeRescheduleAppointmentModal">Cancel</button>
                                <button type="button" class="btn btn-primary w-50" :disabled="loading" @click="rescheduleAppointment">
                                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                                    <span v-else>Reschedule</span>
                                </button>
                            </div>
                            <div v-if="errorMessage" class="text-danger text-center mt-2">{{ errorMessage }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showCancelAppointmentModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-md modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary">
                        <h4 class="modal-title fw-bold">Confirm Appointment Cancellation</h4>
                    </div>
                    <div class="modal-body">
                        <p class="mb-0">Are you sure you want to cancel your appointment on {{ formatDate(selectedAppointment.appointment_date) }} from {{ formatTime(selectedAppointment.slot.slot_time) }}?</p>
                    </div>
                    <div class="modal-footer">
                        <div class="w-100">
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeCancelAppointmentModal">No</button>
                                <button class="btn btn-danger w-50" @click="cancelAppointment" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                                    <span v-else>Yes</span>
                                </button>
                            </div>
                            <div v-if="errorMessage" class="text-danger text-center mt-2">{{ errorMessage }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios";
    import { handleScrollLock } from "@/utils/scroll-lock";
    import { showToast } from "@/utils/toast.js";
    export default {
        name: "AppointmentsTablePatient",
        emits: ['appointmentsChanged'],
        props: {
            title: String,
            appointments: Array,
            past: Boolean,
        },
        data() {
            return {
                selectedAppointment: null,
                searchQuery: "",
                showRescheduleAppointmentModal: false,
                showCancelAppointmentModal: false,
                editableSlot: {},
                selectedSlot: { day: null, index: null },
                slotLabels: ["10:00am - 11:00am", "11:00am - 12:00pm", "12:00pm - 01:00pm", "04:00pm - 05:00pm", "05:00pm - 06:00pm", "06:00pm - 07:00pm",],
                orderedDays: ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                errorMessage: "",
                loading: false,
                rowLoading: {},
            };
        },
        computed: {
            filteredAppointments() {
                if (!this.past || !this.searchQuery.trim()) return this.appointments;
                const q = this.searchQuery.toLowerCase();
                return this.appointments.filter((appointment) => {
                    return (
                        appointment.doctor.department.department_name.toLowerCase().includes(q) ||
                        appointment.doctor.user.full_name.toLowerCase().includes(q) ||
                        this.formatDate(appointment.appointment_date).toLowerCase().includes(q) ||
                        this.formatTime(appointment.slot.slot_time).toLowerCase().includes(q) ||
                        String(this.formatFees(appointment.doctor.fees)).toLowerCase().includes(q) ||
                        (this.past && appointment.status.toLowerCase().includes(q))
                    );
                });
            },
        },
        watch: {
            showRescheduleAppointmentModal: 'updateScrollLock',
            showCancelAppointmentModal: 'updateScrollLock',
        },
        methods: {
            async rescheduleAppointment() {
                if (!this.selectedSlot.day || this.selectedSlot.index === null) {
                    this.errorMessage = "Please select a slot before booking.";
                    return;
                }
                this.errorMessage = "";
                this.loading = true;
                try {
                    const dayIndex = this.orderedDays.indexOf(this.selectedSlot.day);
                    const date = this.getJsDateForSelectedDay(dayIndex);
                    const localDate = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
                    const time = this.slotLabels[this.selectedSlot.index];
                    const payload = {
                        day: this.selectedSlot.day,
                        date: localDate,
                        time: time
                    };
                    const appointmentId = this.selectedAppointment.appointment_id;
                    const response = await axios.put(`/patient/appointment/${appointmentId}`, payload);
                    this.closeRescheduleAppointmentModal();
                    showToast(response.data.message,'success');
                    this.$emit("appointmentsChanged");
                } catch (error) {
                    if (error.response) {
                        this.errorMessage = error.response.data.message;
                    } else {
                        this.errorMessage = "Something went wrong. Please try again later.";
                    }
                } finally {
                    this.loading = false;
                }
            },
            async cancelAppointment() {
                this.errorMessage = "";
                try {
                    this.loading = true;
                    const appointmentId = this.selectedAppointment.appointment_id;
                    const response = await axios.patch(`/patient/appointment/${appointmentId}`);
                    this.closeCancelAppointmentModal();
                    showToast(response.data.message,'success');
                    this.$emit("appointmentsChanged");
                } catch (error) {
                    if (error.response) {
                        this.errorMessage = error.response.data.message;
                    } else {
                        this.errorMessage = "Something went wrong. Please try again later.";
                    }
                } finally {
                    this.loading = false;
                }
            },
            isSlotDisabled(day, index) {
                const slotTimes = [10, 11, 12, 16, 17, 18];
                const slotHour = slotTimes[index];
                const today = new Date();
                const currentDay = today.getDay();
                const monday = new Date(today);
                const diffToMonday = (currentDay === 0 ? -6 : 1 - currentDay);
                monday.setDate(today.getDate() + diffToMonday);
                const dayIndex = this.orderedDays.indexOf(day);
                const slotDate = new Date(monday);
                slotDate.setDate(monday.getDate() + dayIndex);
                slotDate.setHours(slotHour, 0, 0, 0);
                const todayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate());
                if (slotDate < todayStart) return true;
                if (slotDate.toDateString() === today.toDateString() && slotDate < today) {return true;}
                return false;
            },
            buttonClass(day, index, disabled) {
                if (disabled) return "btn-danger";
                const isAvailable = this.editableSlot[day]?.[index];
                if (this.selectedSlot.day === day && this.selectedSlot.index === index) {
                    return "btn-primary";
                }
                return isAvailable ? "btn-success" : "btn-danger";
            },
            selectSlot(day, index) {
                if (!this.editableSlot[day]?.[index]) return;
                this.selectedSlot = { day, index };
            },
            getDateForDay(dayIndex) {
                const today = new Date();
                const currentDay = today.getDay();
                const monday = new Date(today);
                const diffToMonday = (currentDay === 0 ? -6 : 1 - currentDay); 
                monday.setDate(today.getDate() + diffToMonday);
                const target = new Date(monday);
                target.setDate(monday.getDate() + dayIndex);
                return target.toLocaleDateString("en-GB", {day: "2-digit", month: "short", year: "numeric",});
            },
            getJsDateForSelectedDay(dayIndex) {
                const today = new Date();
                const currentDay = today.getDay();
                const monday = new Date(today);
                const diffToMonday = (currentDay === 0 ? -6 : 1 - currentDay);
                monday.setDate(today.getDate() + diffToMonday);
                const target = new Date(monday);
                target.setDate(monday.getDate() + dayIndex);
                return target;
            },
            formatDate(appointment_date) {
                if (!appointment_date) return "";
                const date = new Date(appointment_date);
                const options = { day: '2-digit', month: 'short', year: 'numeric' };
                return date.toLocaleDateString('en-GB', options);
            },
            formatDay(appointment_date) {
                if (!appointment_date) return "";
                const date = new Date(appointment_date);
                const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
                return days[date.getDay()];
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
            formatFees(fees) {
                if (fees == null || isNaN(fees)) return "";
                return `₹${parseFloat(fees).toFixed(2)}`;
            },
            formatStatus(status) {
                return status.charAt(0).toUpperCase() + status.slice(1);
            },
            slotIndexFromTime(timeStr) {
                if (!timeStr) return -1;
                const hh = parseInt(timeStr.split(":")[0], 10);
                const slotTimes = [10, 11, 12, 16, 17, 18];
                return slotTimes.indexOf(hh);
            },
            orderedDayIndexFromDate(dateStr) {
                if (!dateStr) return -1;
                const d = new Date(dateStr);
                if (isNaN(d)) return -1;
                const jsIndex = d.getDay();
                return jsIndex === 0 ? 6 : jsIndex - 1;
            },
            updateScrollLock() {
                handleScrollLock([this.showRescheduleAppointmentModal, this.showCancelAppointmentModal]);
            },
            async openRescheduleAppointmentModal(appointment) {
                this.rowLoading[appointment.appointment_id] = true;
                this.selectedAppointment = appointment;
                try {
                    const response = await axios.get(`/doctor/slot/${this.selectedAppointment.doctor_id}`);
                    this.editableSlot = response.data;
                    const selectedAppointmentDate = this.selectedAppointment.appointment_date;
                    const slotTime = this.selectedAppointment.slot?.slot_time;
                    const dayIdx = this.orderedDayIndexFromDate(selectedAppointmentDate);
                    const dayName = dayIdx >= 0 ? this.orderedDays[dayIdx] : (this.selectedAppointment.slot?.week_day || null);
                    const sIndex = this.slotIndexFromTime(String(slotTime));
                    if (dayName && sIndex >= 0) {this.selectedSlot = { day: dayName, index: sIndex };}
                    this.showRescheduleAppointmentModal = true;
                } catch (error) {
                    if (error.response) {
                        showToast(error.response.data.message,'danger');
                    } else {
                        showToast("Something went wrong. Please try again later.",'danger');
                    }
                } finally {
                    this.rowLoading[appointment.appointment_id] = false;
                }
            },
            closeRescheduleAppointmentModal() {
                this.showRescheduleAppointmentModal = false;
                this.selectedAppointment = null;
                this.selectedSlot = { day: null, index: null };
                this.errorMessage = "";
                this.$nextTick(() => {
                    handleScrollLock([this.showRescheduleAppointmentModal, this.showCancelAppointmentModal]);
                });
            },
            openCancelAppointmentModal(appointment) {
                this.selectedAppointment = appointment;
                this.showCancelAppointmentModal = true;
            },
            closeCancelAppointmentModal() {
                this.showCancelAppointmentModal = false;
                this.selectedAppointment = null;
                this.errorMessage = "";
                this.$nextTick(() => {
                    handleScrollLock([this.showRescheduleAppointmentModal, this.showCancelAppointmentModal]);
                });
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