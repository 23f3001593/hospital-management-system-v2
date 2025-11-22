<template>
    <div class="container my-5">
        <div class="d-flex align-items-center justify-content-between mb-4">
            <h2 class="mb-0 fw-bold">Department of {{ department.department_name }}</h2>
            <router-link to="/patient" class="btn btn-primary"><i class="bi bi-arrow-left me-1"></i> Back</router-link>
        </div>
        <div class="card mb-5">
            <div class="card-body fw-medium p-3">
                <p class="mb-0">{{ department.department_description }}</p>
            </div>
        </div>
        <div class="card search-card">
            <div class="card-body d-flex justify-content-center py-3">
                <div class="input-group search-bar">
                    <span class="input-group-text"><i class="bi bi-search"></i></span>
                    <input type="text" v-model="searchQuery" class="form-control" placeholder="Type to search..."/>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-striped table-hover mb-0 text-center align-middle">
                        <thead>
                            <tr>
                                <th scope="col">Name</th>
                                <th scope="col">Qualifications</th>
                                <th scope="col">Experience</th>
                                <th scope="col">Fees</th>
                                <th scope="col">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="doctor in filteredDoctors" :key="doctor.doctor_id">
                                <td>{{ doctor.user.full_name }}</td>
                                <td>{{ doctor.qualifications }}</td>
                                <td>{{ formatExperience(doctor.practice_start_date) }}</td>
                                <td>{{ formatFees(doctor.fees) }}</td>
                                <td>
                                    <button type="button" class="btn btn-sm btn-primary position-relative" :disabled="rowLoading[doctor.doctor_id]" @click="openSlotModal(doctor)">
                                        <span class="d-inline-block text-center w-100" :class="{ 'invisible': rowLoading[doctor.doctor_id] }">Check Availability</span>
                                        <div v-show="rowLoading[doctor.doctor_id]" class="position-absolute top-50 start-50 translate-middle">
                                            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                        </div>
                                    </button>
                                </td>
                            </tr>
                            <tr v-if="department.doctors?.length > 0 && filteredDoctors.length === 0">
                                <td colspan="5" class="text-muted fst-italic">
                                    No matching records found.
                                </td>
                            </tr>
                            <tr v-if="department.doctors?.length === 0">
                                <td colspan="5" class="text-muted fst-italic">No doctors found.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div v-if="showSlotModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-xl modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary d-flex justify-content-center align-items-center">
                        <h2 class="text-center mb-0 fw-bold">Book Appointment</h2>
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
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeSlotModal">Cancel</button>
                                <button type="button" class="btn btn-primary w-50" :disabled="loading" @click="bookSlot">
                                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                                    <span v-else>Book</span>
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
        name: "DepartmentDoctorsTable",
        props: {
            department: Object,
        },
        data() {
            return {
                searchQuery: "",
                selectedDoctor: null,
                showSlotModal: false,
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
            filteredDoctors() {
                if (!this.searchQuery.trim()) return this.department.doctors;
                const q = this.searchQuery.toLowerCase();
                return this.department.doctors.filter((doctor) => {
                    return (
                        doctor.user.full_name.toLowerCase().includes(q) ||
                        doctor.qualifications.toLowerCase().includes(q) ||
                        String(this.formatExperience(doctor.practice_start_date)).includes(q) ||
                        String(this.formatFees(doctor.fees)).includes(q)
                    );
                });
            },
        },
        watch: {
            showSlotModal: 'updateScrollLock',
        },
        methods: {
            async bookSlot() {
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
                    const id = this.$store.state.user.id;
                    const doctorId = this.selectedDoctor.doctor_id;
                    const response = await axios.post(`/patient/appointment/${id}/${doctorId}`, payload);
                    this.closeSlotModal();
                    showToast(response.data.message,'success');
                    this.$router.push("/patient")
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
            formatExperience(practice_start_date) {
                if (!practice_start_date) return "";
                const startDate = new Date(practice_start_date);
                const today = new Date();
                let years = today.getFullYear() - startDate.getFullYear();
                const months = today.getMonth() - startDate.getMonth();
                if (months < 0 || (months === 0 && today.getDate() < startDate.getDate())) {
                    years--;
                }
                return years > 0 ? `${years} year${years > 1 ? 's' : ''}` : "Less than a year";
            },
            formatFees(fees) {
                if (fees == null || isNaN(fees)) return "";
                return `₹${parseFloat(fees).toFixed(2)}`;
            },
            updateScrollLock() {
                handleScrollLock([this.showSlotModal]);
            },
            async openSlotModal(doctor) {
                this.rowLoading[doctor.doctor_id] = true;
                try {
                    this.selectedDoctor = doctor;
                    const response = await axios.get(`/doctor/slot/${this.selectedDoctor.doctor_id}`);
                    this.editableSlot = response.data;
                    this.showSlotModal = true;
                } catch (error) {
                    if (error.response) {
                        showToast(error.response.data.message,'danger');
                    } else {
                        showToast("Something went wrong. Please try again later.",'danger');
                    }
                } finally {
                    this.rowLoading[doctor.doctor_id] = false;
                }
            },
            closeSlotModal() {
                this.showSlotModal = false;
                this.selectedDoctor = null;
                this.selectedSlot = { day: null, index: null };
                this.errorMessage = "";
            },
        },
    };
</script>

<style scoped>
    .search-card {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    .search-bar {
        width: 100%;
        max-width: 400px;
    }
    .input-group .form-control{
        outline: none !important;
        box-shadow: none !important;
    }
</style>