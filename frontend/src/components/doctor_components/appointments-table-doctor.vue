<template>
    <div class="container my-5">
        <div class="d-flex align-items-center justify-content-between mb-4">
            <h2 class="mb-0 fw-bold">{{ title }}</h2>
        </div>
        <div class="card">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-striped table-hover mb-0 text-center align-middle">
                        <thead>
                            <tr>
                                <th scope="col">S/N</th>
                                <th scope="col">Patient</th>
                                <th scope="col">Date</th>
                                <th scope="col">Day</th>
                                <th scope="col">Time</th>
                                <th scope="col">Patient History</th>
                                <th scope="col">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(appointment,index) in appointments" :key="appointment.appointment_id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ appointment.patient.user.full_name }}</td>
                                <td>{{ formatDate(appointment.appointment_date) }}</td>
                                <td>{{ formatDay(appointment.appointment_date) }}</td>
                                <td>{{ formatTime(appointment.slot.slot_time) }}</td>
                                <td>
                                    <button type="button" class="btn btn-sm btn-primary position-relative" :disabled="rowLoading[appointment.appointment_id]" @click="openViewPatientHistoryModal(appointment)">
                                        <span class="d-inline-block text-center w-100" :class="{ 'invisible': rowLoading[appointment.appointment_id] }">View</span>
                                        <div v-show="rowLoading[appointment.appointment_id]" class="position-absolute top-50 start-50 translate-middle">
                                            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                        </div>
                                    </button>
                                </td>
                                <td>
                                    <button v-if="today" type="button" class="btn btn-sm btn-success me-2" @click="openCompleteAppointmentModal(appointment)">Complete</button>
                                    <button type="button" class="btn btn-sm btn-danger" @click="openCancelAppointmentModal(appointment)">Cancel</button>
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
        <div v-if="showViewPatientHistoryModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary">
                        <h3 class="modal-title fw-bold">{{ selectedAppointment.patient.user.full_name }}'s Treatment History</h3>
                        <button type="button" class="btn-close" @click="closeViewPatientHistoryModal"></button>
                    </div>
                    <div class="modal-body">
                        <div v-for="treatment in selectedPatientTreatments" :key="treatment.treatment_id" class="mb-3">
                            <div class="card h-100">
                                <div class="card-body">
                                    <h5 class="mb-4 text-center">{{ formatDateLong(treatment.appointment.appointment_date) }}</h5>
                                    <p class="mb-2"><strong>Tests:</strong> {{ treatment.tests }}</p>
                                    <p class="mb-2"><strong>Diagnosis:</strong> {{ treatment.diagnosis }}</p>
                                    <p class="mb-2"><strong>Prescription:</strong> {{ treatment.prescription }}</p>
                                    <p class="mb-2"><strong>Medicines:</strong> {{ treatment.medicines }}</p>
                                    <p class="mb-0"><strong>Notes:</strong> {{ treatment.notes }}</p>
                                </div>
                            </div>
                        </div>
                        <div v-if="selectedPatientTreatments.length === 0" class="alert alert-dark text-center fst-italic" role="alert">
                            No treatments found.
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showCompleteAppointmentModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-md modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary d-flex justify-content-center align-items-center">
                        <h2 class="text-center mb-0 fw-bold">Complete Appointment</h2>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="completeAppointment">
                            <div class="mb-3">
                                <label for="tests" class="form-label">
                                    Tests <span class="text-danger">*</span>
                                </label>
                                <textarea
                                    id="tests"
                                    class="form-control"
                                    v-model.trim="form.tests"
                                    :class="{'is-invalid': testsError}"
                                    rows="2"
                                ></textarea>
                                <div v-if="testsError" class="text-danger mt-1">{{ testsError }}</div>
                            </div>
                            <div class="mb-3">
                                <label for="diagnosis" class="form-label">
                                    Diagnosis <span class="text-danger">*</span>
                                </label>
                                <textarea
                                    id="diagnosis"
                                    class="form-control"
                                    v-model.trim="form.diagnosis"
                                    :class="{'is-invalid': diagnosisError}"
                                    rows="3"
                                ></textarea>
                                <div v-if="diagnosisError" class="text-danger mt-1">{{ diagnosisError }}</div>
                            </div>
                            <div class="mb-3">
                                <label for="prescription" class="form-label">
                                    Prescription <span class="text-danger">*</span>
                                </label>
                                <textarea
                                    id="prescription"
                                    class="form-control"
                                    v-model.trim="form.prescription"
                                    :class="{'is-invalid': prescriptionError}"
                                    rows="4"
                                ></textarea>
                                <div v-if="prescriptionError" class="text-danger mt-1">{{ prescriptionError }}</div>
                            </div>
                            <div class="mb-3">
                                <label for="medicines" class="form-label">
                                    Medicines <span class="text-danger">*</span>
                                </label>
                                <textarea
                                    id="medicines"
                                    class="form-control"
                                    v-model.trim="form.medicines"
                                    :class="{'is-invalid': medicinesError}"
                                    rows="3"
                                ></textarea>
                                <div v-if="medicinesError" class="text-danger mt-1">{{ medicinesError }}</div>
                            </div>
                            <div class="mb-3">
                                <label for="notes" class="form-label">
                                    Notes <span class="text-danger">*</span>
                                </label>
                                <textarea
                                    id="notes"
                                    class="form-control"
                                    v-model.trim="form.notes"
                                    :class="{'is-invalid': notesError}"
                                    rows="2"
                                ></textarea>
                                <div v-if="notesError" class="text-danger mt-1">{{ notesError }}</div>
                            </div>
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeCompleteAppointmentModal">Cancel</button>
                                <button type="submit" class="btn btn-primary w-50" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                                    <span v-else>Complete</span>
                                </button>
                            </div>
                        </form>
                        <div v-if="errorMessage" class="text-danger text-center mt-2">{{ errorMessage }}</div>
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
                        <p class="mb-0">Are you sure you want to cancel {{ selectedAppointment.patient.user.full_name }}'s appointment on {{ formatDate(selectedAppointment.appointment_date) }} from {{ formatTime(selectedAppointment.slot.slot_time) }}?</p>
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
        name: "AppointmentsTableDoctor",
        emits: ['appointmentsChanged'],
        props: {
            title: String,
            appointments: Array,
            today: Boolean,
        },
        data() {
            return {
                form: {
                    tests: "",
                    diagnosis: "",
                    prescription: "",
                    medicines: "",
                    notes: "",
                },
                selectedAppointment: null,
                selectedPatientTreatments: [],
                showViewPatientHistoryModal: false,
                showCompleteAppointmentModal: false,
                showCancelAppointmentModal: false,
                errorMessage: "",
                testsError: "",
                diagnosisError: "",
                prescriptionError: "",
                medicinesError: "",
                notesError: "",
                loading: false,
                rowLoading: {},
            };
        },
        watch: {
            showViewPatientHistoryModal: 'updateScrollLock',
            showCompleteAppointmentModal: 'updateScrollLock',
            showCancelAppointmentModal: 'updateScrollLock',
        },
        methods: {
            async completeAppointment() {
                this.clearAllErrors();
                let valid = true;
                if (!this.form.tests) {
                    this.testsError = "Tests is required.";
                    valid = false;
                }
                if (!this.form.diagnosis) {
                    this.diagnosisError = "Diagnosis is required.";
                    valid = false;
                }
                if (!this.form.prescription) {
                    this.prescriptionError = "Prescription is required.";
                    valid = false;
                }
                if (!this.form.medicines) {
                    this.medicinesError = "Medicines is required.";
                    valid = false;
                }
                if (!this.form.notes) {
                    this.notesError = "Notes is required.";
                    valid = false;
                }
                if (!valid) return;
                try {
                    this.loading = true;
                    const payload = {
                        tests: this.form.tests,
                        diagnosis: this.form.diagnosis,
                        prescription: this.form.prescription,
                        medicines: this.form.medicines,
                        notes: this.form.notes,
                    };
                    const appointmentId = this.selectedAppointment.appointment_id;
                    const response = await axios.post(`/doctor/treatment/${appointmentId}`, payload);
                    this.closeCompleteAppointmentModal();
                    showToast(response.data.message,'success');
                    this.$emit('appointmentsChanged');
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
            formatHour(hour, minute) {
                const suffix = hour >= 12 ? "pm" : "am";
                const normalizedHour = hour % 12 || 12;
                const paddedHour = normalizedHour.toString().padStart(2, "0");
                const paddedMinute = minute.toString().padStart(2, "0");
                return `${paddedHour}:${paddedMinute}${suffix}`;
            },
            formatDate(appointment_date) {
                if (!appointment_date) return "";
                const date = new Date(appointment_date);
                const options = { day: '2-digit', month: 'short', year: 'numeric' };
                return date.toLocaleDateString('en-GB', options);
            },
            formatDateLong(appointment_date) {
                if (!appointment_date) return "";
                const date = new Date(appointment_date);
                const options = { day: '2-digit', month: 'long', year: 'numeric' };
                return date.toLocaleDateString('en-GB', options);
            },
            formatDay(appointment_date) {
                if (!appointment_date) return "";
                const date = new Date(appointment_date);
                const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
                return days[date.getDay()];
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
            updateScrollLock() {
                handleScrollLock([this.showViewPatientHistoryModal, this.showCompleteAppointmentModal, this.showCancelAppointmentModal]);
            },
            async openViewPatientHistoryModal(appointment) {
                this.rowLoading[appointment.appointment_id] = true;
                this.selectedAppointment = appointment;
                try {
                    const response = await axios.get(`/patient/treatments/${this.selectedAppointment.patient.user.id}`);
                    this.selectedPatientTreatments = response.data.treatments;
                    this.selectedPatientTreatments.sort((a, b) => {
                        return new Date(b.appointment.appointment_date) - new Date(a.appointment.appointment_date);
                    });
                    this.showViewPatientHistoryModal = true;
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
            closeViewPatientHistoryModal() {
                this.showViewPatientHistoryModal = false;
                this.selectedAppointment = null;
                this.selectedPatientTreatments = [];
                this.errorMessage = "";
                this.$nextTick(() => {
                    handleScrollLock([this.showViewPatientHistoryModal, this.showCompleteAppointmentModal, this.showCancelAppointmentModal]);
                });
            },
            openCompleteAppointmentModal(appointment) {
                this.selectedAppointment = appointment;
                this.showCompleteAppointmentModal = true;
            },
            closeCompleteAppointmentModal() {
                this.showCompleteAppointmentModal = false;
                this.selectedAppointment = null;
                this.form.tests = "";
                this.form.diagnosis = "";
                this.form.prescription = "";
                this.form.medicines = "";
                this.form.notes = "";
                this.clearAllErrors();
                this.$nextTick(() => {
                    handleScrollLock([this.showViewPatientHistoryModal, this.showCompleteAppointmentModal, this.showCancelAppointmentModal]);
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
                    handleScrollLock([this.showViewPatientHistoryModal, this.showCompleteAppointmentModal, this.showCancelAppointmentModal]);
                });
            },
            clearAllErrors() {
                this.errorMessage = "";
                this.testsError = "";
                this.diagnosisError = "";
                this.prescriptionError = "";
                this.medicinesError = "";
                this.notesError = "";
            },
        },
    };
</script>

<style scoped>
    .modal-header .btn-close {
        filter: invert(1) brightness(200%);
        opacity: 1;
    }
    .modal-header .btn-close:focus, .modal-header .btn-close:active {
        box-shadow: none !important;
    }
</style>