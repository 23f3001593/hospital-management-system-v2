<template>
    <div class="container my-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="mb-0 fw-bold">{{ title }}</h2>
            <input type="text" v-model="searchQuery" class="form-control" placeholder="Type to search..."/>
            <router-link v-if="!archived" to="/admin/doctor/create" class="btn btn-primary">+ Create Doctor</router-link>
        </div>
        <div class="card">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-striped table-hover mb-0 text-center">
                        <thead class="align-middle">
                            <tr>
                                <th scope="col">ID</th>
                                <th scope="col">Username</th>
                                <th scope="col">Full Name</th>
                                <th scope="col">Email</th>
                                <th scope="col">Phone Number</th>
                                <th scope="col">Department</th>
                                <th scope="col">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="doctor in filteredDoctors" :key="doctor.doctor_id">
                                <td>{{ doctor.doctor_id }}</td>
                                <td>{{ doctor.user.username }}</td>
                                <td>{{ doctor.user.full_name }}</td>
                                <td>{{ doctor.user.email }}</td>
                                <td>{{ formatPhoneNumber(doctor.user.phone_number) }}</td>
                                <td>{{ doctor.department.department_name }}</td>
                                <td class="btn-group btn-group-sm">
                                    <button class="btn btn-primary" @click="openReadDoctorModal(doctor)" title="Show More">
                                        <i class="bi bi-eye-fill"></i>
                                    </button>
                                    <button v-if="!archived" class="btn btn-danger" @click="openDeleteDoctorModal(doctor)" title="Delete">
                                        <i class="bi bi-trash3"></i>
                                    </button>
                                </td>
                            </tr>
                            <tr v-if="doctors.length > 0 && filteredDoctors.length === 0">
                                <td colspan="7" class="text-muted fst-italic">
                                    No matching records found.
                                </td>
                            </tr>
                            <tr v-if="doctors.length === 0">
                                <td colspan="7" class="text-muted fst-italic">No doctors found.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div v-if="showReadDoctorModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary">
                        <h3 class="modal-title fw-bold">{{ selectedDoctor.user.full_name }}</h3>
                        <button type="button" class="btn-close" @click="closeReadDoctorModal"></button>
                    </div>
                    <div class="modal-body">
                        <p class="mb-2"><strong>ID:</strong> #{{ selectedDoctor.doctor_id }}</p>
                        <p class="mb-2"><strong>Username:</strong> {{ selectedDoctor.user.username }}</p>
                        <p class="mb-2"><strong>Fullname:</strong> {{ selectedDoctor.user.full_name }}</p>
                        <p class="mb-2"><strong>Email:</strong> {{ selectedDoctor.user.email }}</p>
                        <p class="mb-2"><strong>Phone Number:</strong> {{ formatPhoneNumber(selectedDoctor.user.phone_number) }}</p>
                        <p class="mb-2"><strong>Department:</strong> {{ selectedDoctor.department.department_name }}</p>
                        <p class="mb-2"><strong>License Number:</strong> {{ selectedDoctor.license_number }}</p>
                        <p class="mb-2"><strong>Qualifications:</strong> {{ selectedDoctor.qualifications }}</p>
                        <p class="mb-2"><strong>Experience:</strong> {{ formatExperience(selectedDoctor.practice_start_date) }}</p>
                        <p class="mb-0"><strong>Fees:</strong> {{ formatFees(selectedDoctor.fees) }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showDeleteDoctorModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-md modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary">
                        <h4 class="modal-title fw-bold">Confirm Doctor Deletion</h4>
                    </div>
                    <div class="modal-body">
                        <p class="mb-0">Are you sure you want to delete {{ selectedDoctor.user.username }}?</p>
                    </div>
                    <div class="modal-footer">
                        <div class="w-100">
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeDeleteDoctorModal">Cancel</button>
                                <button class="btn btn-danger w-50" @click="deleteDoctor(selectedDoctor)" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                                    <span v-else>Delete</span>
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
        name: "DoctorsTable",
        emits: ['doctorsChanged'],
        props: {
            title: String,
            doctors: Array,
            archived: Boolean,
        },
        data() {
            return {
                searchQuery: "",
                selectedDoctor: null,
                showReadDoctorModal: false,
                showDeleteDoctorModal: false,
                errorMessage: "",
                loading: false,
            };
        },
        computed: {
            filteredDoctors() {
                if (!this.searchQuery.trim()) return this.doctors;
                const q = this.searchQuery.toLowerCase();
                return this.doctors.filter((doctor) => {
                    return (
                        String(doctor.doctor_id).includes(q) ||
                        doctor.user.username.toLowerCase().includes(q) ||
                        doctor.user.full_name.toLowerCase().includes(q) ||
                        doctor.user.email.toLowerCase().includes(q) ||
                        doctor.user.phone_number.toLowerCase().includes(q) ||
                        doctor.department.department_name.toLowerCase().includes(q)
                    );
                });
            },
        },
        watch: {
            showReadDoctorModal: 'updateScrollLock',
            showDeleteDoctorModal: 'updateScrollLock',
        },
        methods: {
            async deleteDoctor(doctor) {
                this.errorMessage = "";
                try {
                    this.loading = true;
                    const response = await axios.patch(`/doctor/${doctor.doctor_id}`);
                    this.closeDeleteDoctorModal();
                    showToast('Doctor deleted successfully.','success');
                    this.$emit("doctorsChanged");
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
            formatPhoneNumber(phone) {
                if (!phone) return "";
                const country = phone.slice(0, 3);
                const firstPart = phone.slice(3, 8);
                const lastPart = phone.slice(8);
                return `${country} ${firstPart} ${lastPart}`;
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
                handleScrollLock([this.showReadDoctorModal, this.showDeleteDoctorModal]);
            },
            openReadDoctorModal(doctor) {
                this.selectedDoctor = doctor;
                this.showReadDoctorModal = true;
            },
            closeReadDoctorModal() {
                this.showReadDoctorModal = false;
                this.selectedDoctor = null;
            },
            openDeleteDoctorModal(doctor) {
                this.selectedDoctor = doctor;
                this.showDeleteDoctorModal = true;
            },
            closeDeleteDoctorModal() {
                this.showDeleteDoctorModal = false;
                this.selectedDoctor = null;
                this.errorMessage = "";
            },
        },
    };
</script>

<style scoped>
    input.form-control {
        max-width: 400px;
    }
    .modal-header .btn-close {
        filter: invert(1) brightness(200%);
        opacity: 1;
    }
    .modal-header .btn-close:focus, .modal-header .btn-close:active {
        box-shadow: none !important;
    }
    td.btn-group, td.btn-group-sm {
        display: table-cell !important;
        border-radius: 0 !important;
    }
</style>