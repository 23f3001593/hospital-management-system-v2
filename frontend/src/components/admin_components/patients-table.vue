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
                                <th scope="col">Username</th>
                                <th scope="col">Full Name</th>
                                <th scope="col">Email</th>
                                <th scope="col">Phone Number</th>
                                <th scope="col">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="patient in filteredPatients" :key="patient.patient_id">
                                <td>{{ patient.patient_id }}</td>
                                <td>{{ patient.user.username }}</td>
                                <td>{{ patient.user.full_name }}</td>
                                <td>{{ patient.user.email }}</td>
                                <td>{{ formatPhoneNumber(patient.user.phone_number) }}</td>
                                <td class="btn-group btn-group-sm">
                                    <button class="btn btn-primary" @click="openReadPatientModal(patient)" title="Show More">
                                        <i class="bi bi-eye-fill"></i>
                                    </button>
                                    <button v-if="!archived" class="btn btn-danger" @click="openDeletePatientModal(patient)" title="Delete">
                                        <i class="bi bi-trash3"></i>
                                    </button>
                                </td>
                            </tr>
                            <tr v-if="patients.length > 0 && filteredPatients.length === 0">
                                <td colspan="6" class="text-muted fst-italic">
                                    No matching records found.
                                </td>
                            </tr>
                            <tr v-if="patients.length === 0">
                                <td colspan="6" class="text-muted fst-italic">No patients found.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div v-if="showReadPatientModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary">
                        <h3 class="modal-title fw-bold">{{ selectedPatient.user.full_name }}</h3>
                        <button type="button" class="btn-close" @click="closeReadPatientModal"></button>
                    </div>
                    <div class="modal-body">
                        <p class="mb-2"><strong>ID:</strong> #{{ selectedPatient.patient_id }}</p>
                        <p class="mb-2"><strong>Username:</strong> {{ selectedPatient.user.username }}</p>
                        <p class="mb-2"><strong>Fullname:</strong> {{ selectedPatient.user.full_name }}</p>
                        <p class="mb-2"><strong>Email:</strong> {{ selectedPatient.user.email }}</p>
                        <p class="mb-2"><strong>Phone Number:</strong> {{ formatPhoneNumber(selectedPatient.user.phone_number) }}</p>
                        <p class="mb-2"><strong>DOB:</strong> {{ formatDob(selectedPatient.dob) }}</p>
                        <p class="mb-2"><strong>Age:</strong> {{ formatAge(selectedPatient.dob) }}</p>
                        <p class="mb-2"><strong>Gender:</strong> {{ formatGender(selectedPatient.gender) }}</p>
                        <p class="mb-2"><strong>Address:</strong> {{ selectedPatient.address }}</p>
                        <p class="mb-0"><strong>Pincode:</strong> {{ selectedPatient.pincode }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showDeletePatientModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-md modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary">
                        <h4 class="modal-title fw-bold">Confirm Patient Deletion</h4>
                    </div>
                    <div class="modal-body">
                        <p class="mb-0">Are you sure you want to delete {{ selectedPatient.user.username }}?</p>
                    </div>
                    <div class="modal-footer">
                        <div class="w-100">
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeDeletePatientModal">Cancel</button>
                                <button class="btn btn-danger w-50" @click="deletePatient(selectedPatient)" :disabled="loading">
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
        name: "PatientsTable",
        emits: ['patientsChanged'],
        props: {
            title: String,
            patients: Array,
            archived: Boolean,
        },
        data() {
            return {
                searchQuery: "",
                selectedPatient: null,
                showReadPatientModal: false,
                showDeletePatientModal: false,
                errorMessage: "",
                loading: false,
            };
        },
        computed: {
            filteredPatients() {
                if (!this.searchQuery.trim()) return this.patients;
                const q = this.searchQuery.toLowerCase();
                return this.patients.filter((patient) => {
                    return (
                        String(patient.patient_id).includes(q) ||
                        patient.user.username.toLowerCase().includes(q) ||
                        patient.user.full_name.toLowerCase().includes(q) ||
                        patient.user.email.toLowerCase().includes(q) ||
                        patient.user.phone_number.toLowerCase().includes(q)
                    );
                });
            },
        },
        watch: {
            showReadPatientModal: 'updateScrollLock',
            showDeletePatientModal: 'updateScrollLock',
        },
        methods: {
            async deletePatient(patient) {
                this.errorMessage = "";
                try {
                    this.loading = true;
                    const response = await axios.patch(`/patient/${patient.patient_id}`);
                    this.closeDeletePatientModal();
                    showToast('Patient deleted successfully.','success');
                    this.$emit("patientsChanged");
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
            formatDob(dob) {
                if (!dob) return "";
                const date = new Date(dob);
                const options = { day: '2-digit', month: 'long', year: 'numeric' };
                return date.toLocaleDateString('en-GB', options);
            },
            formatAge(dob) {
                if (!dob) return "";
                const birthDate = new Date(dob);
                const today = new Date();
                const diffMs = today - birthDate;
                const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
                if (diffDays < 1) return "Less than a day";
                let years = today.getFullYear() - birthDate.getFullYear();
                let months = today.getMonth() - birthDate.getMonth();
                let days = today.getDate() - birthDate.getDate();
                if (days < 0) {
                    months--;
                    const prevMonth = new Date(today.getFullYear(), today.getMonth(), 0);
                    days += prevMonth.getDate();
                }
                if (months < 0) {
                    years--;
                    months += 12;
                }
                if (years > 0) {
                    return `${years} year${years > 1 ? "s" : ""}`;
                } else if (months > 0) {
                    return `${months} month${months > 1 ? "s" : ""}`;
                } else if (days > 0) {
                    return `${days} day${days > 1 ? "s" : ""}`;
                } else {
                    return "Less than a day";
                }
            },
            formatGender(value) {
                if (!value) return "";
                return value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
            },
            updateScrollLock() {
                handleScrollLock([this.showReadPatientModal, this.showDeletePatientModal]);
            },
            openReadPatientModal(patient) {
                this.selectedPatient = patient;
                this.showReadPatientModal = true;
            },
            closeReadPatientModal() {
                this.showReadPatientModal = false;
                this.selectedPatient = null;
            },
            openDeletePatientModal(patient) {
                this.selectedPatient = patient;
                this.showDeletePatientModal = true;
            },
            closeDeletePatientModal() {
                this.showDeletePatientModal = false;
                this.selectedPatient = null;
                this.errorMessage = "";
            },
        },
    };
</script>

<style scoped>
    .search-bar {
        width: 100%;
        width: 300px;
    }
    .input-group .form-control{
        outline: none !important;
        box-shadow: none !important;
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