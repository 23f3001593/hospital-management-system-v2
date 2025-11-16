<template>
    <div class="container my-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="mb-0 fw-bold">{{ title }}</h2>
            <button v-if="!archived" class="btn btn-primary" @click="openCreateDepartmentModal">+ Create Department</button>
        </div>
        <div class="row">
            <div v-for="department in departments" :key="department.department_id" class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">{{ department.department_name }}</h5>
                        <div v-if="!archived" class="btn-group btn-group-sm">
                            <button class="btn btn-outline-light" @click="openUpdateDepartmentModal(department)" title="Update">
                                <i class="bi bi-pencil-square"></i>
                            </button>
                            <button class="btn btn-outline-light" @click="openDeleteDepartmentModal(department)" title="Delete">
                                <i class="bi bi-trash3"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <p class="mb-2"><strong>ID:</strong> #{{ department.department_id }}</p>
                        <p class="mb-2"><strong>HOD ID:</strong> {{ department.hod_id ? '#' + department.hod_id : 'N/A' }}</p>
                        <p class="mb-2"><strong>HOD:</strong> {{ department.hod_name ? department.hod_name : 'N/A' }}</p>
                        <p class="mb-0">
                            <strong>Description:</strong>
                            <span class="description-text">{{ department.department_description }}</span>
                            <span v-if="overflowingDepartments.includes(department.department_id)" class="show-more text-primary text-decoration-none" role="button" tabindex="0" @click="openReadDepartmentModal(department)">Show more</span>
                        </p>
                    </div>
                </div>
            </div>
            <div v-if="departments.length === 0" class="alert alert-dark text-center fst-italic col-12" role="alert">
                No departments found.
            </div>
        </div>
        <div v-if="showCreateDepartmentModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-md modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary d-flex justify-content-center align-items-center">
                        <h2 class="text-center mb-0 fw-bold">Create Department</h2>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="createDepartment">
                            <div class="mb-3">
                                <label for="department_name" class="form-label">
                                    Department Name <span class="text-danger">*</span>
                                </label>
                                <input
                                    type="text"
                                    id="department_name"
                                    class="form-control"
                                    v-model.trim="form.department_name"
                                    :class="{'is-invalid': nameError}"
                                />
                                <div v-if="nameError" class="text-danger mt-1">{{ nameError }}</div>
                            </div>
                            <div class="mb-3">
                                <label for="department_description" class="form-label">
                                    Department Description <span class="text-danger">*</span>
                                </label>
                                <textarea
                                    id="department_description"
                                    class="form-control"
                                    v-model.trim="form.department_description"
                                    :class="{'is-invalid': descriptionError}"
                                    rows="5"
                                ></textarea>
                                <div v-if="descriptionError" class="text-danger mt-1">{{ descriptionError }}</div>
                            </div>
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeCreateDepartmentModal">Cancel</button>
                                <button type="submit" class="btn btn-primary w-50" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                                    <span v-else>Create</span>
                                </button>
                            </div>
                        </form>
                        <div v-if="errorMessage" class="text-danger text-center mt-2">{{ errorMessage }}</div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showReadDepartmentModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary">
                        <h3 class="modal-title fw-bold">{{ selectedDepartment.department_name }}</h3>
                        <button type="button" class="btn-close" @click="closeReadDepartmentModal"></button>
                    </div>
                    <div class="modal-body">
                        <p class="mb-3"><strong>ID:</strong> #{{ selectedDepartment.department_id }}</p>
                        <p class="mb-3"><strong>HOD ID:</strong> {{ selectedDepartment.hod_id ? '#' + selectedDepartment.hod_id : 'N/A' }}</p>
                        <p class="mb-3"><strong>HOD:</strong> {{ selectedDepartment.hod_name ? selectedDepartment.hod_name : 'N/A' }}</p>
                        <p class="mb-3"><strong>Description:</strong> {{ selectedDepartment.department_description }}</p>
                        <p class="mb-0"><strong>Doctors:</strong> <span v-if="!selectedDepartment.doctors.length">N/A</span></p>
                        <ul>
                            <li v-for="doctor in selectedDepartment.doctors" :key="doctor.doctor_id">{{ doctor.user.full_name }}</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showUpdateDepartmentModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-md modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary d-flex justify-content-center align-items-center">
                        <h2 class="text-center mb-0 fw-bold">Update Department</h2>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="updateDepartment(selectedDepartment)">
                            <div class="mb-3">
                                <label for="department_name" class="form-label">
                                    Department Name <span class="text-danger">*</span>
                                </label>
                                <input
                                    type="text"
                                    id="department_name"
                                    class="form-control"
                                    v-model.trim="form.department_name"
                                    :placeholder="selectedDepartment.department_name"
                                    :class="{'is-invalid': nameError}"
                                />
                                <div v-if="nameError" class="text-danger mt-1">{{ nameError }}</div>
                            </div>
                            <div class="mb-3">
                                <label for="hod" class="form-label">HOD</label>
                                <select id="hod" class="form-select" v-model="form.hod_id" :disabled="!selectedDepartment.doctors.some(d => d.user?.full_name)">
                                    <option v-for="doctor in selectedDepartment.doctors" :key="doctor.doctor_id" :value="doctor.doctor_id">
                                        {{ doctor.user.full_name }}
                                    </option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="department_description" class="form-label">
                                    Department Description <span class="text-danger">*</span>
                                </label>
                                <textarea
                                    id="department_description"
                                    class="form-control"
                                    v-model.trim="form.department_description"
                                    :placeholder="selectedDepartment.department_description"
                                    :class="{'is-invalid': descriptionError}"
                                    rows="5"
                                ></textarea>
                                <div v-if="descriptionError" class="text-danger mt-1">{{ descriptionError }}</div>
                            </div>
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeUpdateDepartmentModal">Cancel</button>
                                <button type="submit" class="btn btn-primary w-50" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                                    <span v-else>Update</span>
                                </button>
                            </div>
                        </form>
                        <div v-if="errorMessage" class="text-danger text-center mt-2">{{ errorMessage }}</div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showDeleteDepartmentModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-md modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary">
                        <h4 class="modal-title fw-bold">Confirm Department Deletion</h4>
                    </div>
                    <div class="modal-body">
                        <p class="mb-0">Are you sure you want to delete the {{ selectedDepartment.department_name }} department?</p>
                    </div>
                    <div class="modal-footer">
                        <div class="w-100">
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeDeleteDepartmentModal">Cancel</button>
                                <button class="btn btn-danger w-50" @click="deleteDepartment(selectedDepartment)" :disabled="loading">
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
        name: "DepartmentsGrid",
        emits: ['departmentsChanged'],
        props: {
            title: String,
            departments: Array,
            archived: Boolean,
        },
        data() {
            return {
                form: {
                    department_name: "",
                    department_description: "",
                    hod_id: "",
                },
                selectedDepartment: null,
                showCreateDepartmentModal: false,
                showReadDepartmentModal: false,
                showUpdateDepartmentModal: false,
                showDeleteDepartmentModal: false,
                overflowingDepartments: [],
                maxLength: 125,
                errorMessage: "",
                nameError: "",
                descriptionError: "",
                loading: false,
            };
        },
        watch: {
            departments() {
                this.$nextTick(() => this.checkOverflow());
            },
            "form.department_name"(value) {
                const regex = /^[A-Za-z\s]{1,}$/;
                if (!value) this.nameError = "";
                else if (!regex.test(value)) this.nameError = "Please enter a valid Department Name.";
                else this.nameError = "";
            },
            showCreateDepartmentModal: 'updateScrollLock',
            showReadDepartmentModal: 'updateScrollLock',
            showUpdateDepartmentModal: 'updateScrollLock',
            showDeleteDepartmentModal: 'updateScrollLock',
        },
        methods: {
            async createDepartment() {
                this.clearAllErrors();
                let valid = true;
                if (!this.form.department_name) {
                    this.nameError = "Department Name is required.";
                    valid = false;
                }
                if (!this.form.department_description) {
                    this.descriptionError = "Department Description is required.";
                    valid = false;
                }
                if (this.form.department_name) {
                    if (this.form.department_name.length > 100) {
                        this.nameError = "Department Name can be upto 100 characters long.";
                        valid = false;
                    }
                }
                if (!valid) return;
                try {
                    this.loading = true;
                    const payload = {
                        department_name: this.form.department_name,
                        department_description: this.form.department_description,
                    };
                    const response = await axios.post('/admin/department', payload);
                    this.closeCreateDepartmentModal();
                    showToast(response.data.message,'success');
                    this.$emit('departmentsChanged');
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
            async updateDepartment(department) {
                this.clearAllErrors();
                let valid = true;
                if (!this.form.department_name) {
                    this.nameError = "Department Name is required.";
                    valid = false;
                }
                if (!this.form.department_description) {
                    this.descriptionError = "Department Description is required.";
                    valid = false;
                }
                if (this.form.department_name) {
                    if (this.form.department_name.length > 100) {
                        this.nameError = "Department Name can be upto 100 characters long.";
                        valid = false;
                    }
                }
                if (!valid) return;
                try {
                    this.loading = true;
                    const payload = {
                        department_name: this.form.department_name,
                        department_description: this.form.department_description,
                    };
                    const response = await axios.put(`/admin/department/${department.department_id}`, payload);
                    if (this.form.hod_id) {
                        await axios.put(`/admin/assign-hod/${department.department_id}/${this.form.hod_id}`);
                    }
                    this.closeUpdateDepartmentModal();
                    showToast(response.data.message,'success');
                    this.$emit('departmentsChanged');
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
            async deleteDepartment(department) {
                this.errorMessage = "";
                try {
                    this.loading = true;
                    const response = await axios.patch(`/admin/department/${department.department_id}`);
                    this.closeDeleteDepartmentModal();
                    showToast(response.data.message,'success');
                    this.$emit("departmentsChanged");
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
            isTextOverflowing(el) {
                if (!el) return false;
                return el.scrollHeight > el.clientHeight + 1;
            },
            checkOverflow() {
                this.overflowingDepartments = [];
                const descriptionEls = this.$el.querySelectorAll(".description-text");
                descriptionEls.forEach((el, index) => {
                    if (this.isTextOverflowing(el)) {
                        const deptId = this.departments[index].department_id;
                        this.overflowingDepartments.push(deptId);
                    }
                });
            },
            updateScrollLock() {
                handleScrollLock([this.showCreateDepartmentModal, this.showReadDepartmentModal, this.showUpdateDepartmentModal, this.showDeleteDepartmentModal]);
            },
            openCreateDepartmentModal() {
                this.showCreateDepartmentModal = true;
            },
            closeCreateDepartmentModal() {
                this.showCreateDepartmentModal = false;
                this.form.department_name = "";
                this.form.department_description = "";
                this.clearAllErrors();
                this.$nextTick(() => {
                    handleScrollLock([this.showCreateDepartmentModal, this.showReadDepartmentModal, this.showUpdateDepartmentModal, this.showDeleteDepartmentModal]);
                });
            },
            openReadDepartmentModal(department) {
                this.selectedDepartment = department;
                this.showReadDepartmentModal = true;
            },
            closeReadDepartmentModal() {
                this.showReadDepartmentModal = false;
                this.selectedDepartment = null;
            },
            openUpdateDepartmentModal(department) {
                this.selectedDepartment = department;
                this.form.department_name = department.department_name;
                this.form.department_description = department.department_description;
                this.form.hod_id = department.hod_id || "";
                this.showUpdateDepartmentModal = true;
            },
            closeUpdateDepartmentModal() {
                this.showUpdateDepartmentModal = false;
                this.selectedDepartment = null;
                this.form.department_name = "";
                this.form.department_description = "";
                this.form.hod_id = "";
                this.clearAllErrors();
                this.$nextTick(() => {
                    handleScrollLock([this.showCreateDepartmentModal, this.showReadDepartmentModal, this.showUpdateDepartmentModal, this.showDeleteDepartmentModal]);
                });
            },
            openDeleteDepartmentModal(department) {
                this.selectedDepartment = department;
                this.showDeleteDepartmentModal = true;
            },
            closeDeleteDepartmentModal() {
                this.showDeleteDepartmentModal = false;
                this.selectedDepartment = null;
                this.errorMessage = "";
                this.$nextTick(() => {
                    handleScrollLock([this.showCreateDepartmentModal, this.showReadDepartmentModal, this.showUpdateDepartmentModal, this.showDeleteDepartmentModal]);
                });
            },
            clearAllErrors() {
                this.errorMessage = "";
                this.nameError = "";
                this.descriptionError = "";
            },
        },
        mounted() {
            this.$nextTick(() => {
                this.checkOverflow();
            });
        },
    };
</script>

<style scoped>
    .show-more {
        color: var(--bs-primary);
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s ease-in-out;
    }
    .description-text {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.5;
        max-height: calc(1.5em * 3);
    }
    .modal-header .btn-close {
        filter: invert(1) brightness(200%);
        opacity: 1;
    }
    .modal-header .btn-close:focus, .modal-header .btn-close:active {
        box-shadow: none !important;
    }
</style>