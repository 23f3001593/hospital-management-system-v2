<template>
    <div class="create-doctor-container my-5">
        <div class="create-doctor-card">
            <h1 class="text-center mb-4 text-primary fw-bold">Create Doctor</h1>
            <form @submit.prevent="createDoctor">
                <div class="mb-3">
                    <label for="fullname" class="form-label">
                        Full Name <span class="text-danger">*</span>
                    </label>
                    <input
                        type="text"
                        id="fullname"
                        class="form-control"
                        v-model.trim="form.fullname"
                        :class="{'is-invalid': fullnameError}"
                        autocomplete="name"
                    />
                    <div v-if="fullnameError" class="text-danger mt-1">{{ fullnameError }}</div>
                </div>
                <div class="mb-3">
                    <label for="email_name" class="form-label">
                        Email <span class="text-danger">*</span>
                    </label>
                    <div class="input-group">
                        <input
                            type="text"
                            id="email_name"
                            class="form-control"
                            v-model.trim="form.email_name"
                            :class="{'is-invalid': emailError}"
                            autocomplete="email"
                        />
                        <select
                            id="email_domain"
                            class="form-select email-domain"
                            v-model="form.email_domain"
                        >
                            <option value="@example.com">@example.com</option>
                            <option value="@gmail.com">@gmail.com</option>
                        </select>
                    </div>
                    <div v-if="emailError" class="text-danger mt-1">{{ emailError }}</div>
                </div>
                <div class="mb-3">
                    <label for="phone_number" class="form-label">
                        Phone Number <span class="text-danger">*</span>
                    </label>
                    <div class="input-group">
                        <select
                            id="country_code"
                            class="form-select country-code"
                            v-model="form.country_code"
                        >
                            <option value="+91">+91</option>
                        </select>
                        <input
                            type="text"
                            id="phone_number"
                            class="form-control"
                            v-model.trim="form.phone_number"
                            :class="{'is-invalid': phoneError}"
                            maxlength="10"
                            autocomplete="tel-national"
                        />
                    </div>
                    <div v-if="phoneError" class="text-danger mt-1">{{ phoneError }}</div>
                </div>
                <div class="mb-3">
                    <label for="qualifications" class="form-label">
                        Qualifications <span class="text-danger">*</span>
                    </label>
                    <textarea
                        id="qualifications"
                        class="form-control"
                        v-model.trim="form.qualifications"
                        :class="{'is-invalid': qualificationsError}"
                        rows="2"
                    ></textarea>
                    <div v-if="qualificationsError" class="text-danger mt-1">{{ qualificationsError }}</div>
                </div>
                <div class="mb-3">
                    <label for="license_number" class="form-label">
                        License Number <span class="text-danger">*</span>
                    </label>
                    <input
                        type="text"
                        id="license_number"
                        class="form-control"
                        v-model.trim="form.license_number"
                        :class="{'is-invalid': licenseNumberError}"
                    />
                    <div v-if="licenseNumberError" class="text-danger mt-1">{{ licenseNumberError }}</div>
                </div>
                <div class="mb-3">
                    <label for="department" class="form-label">
                        Department <span class="text-danger">*</span>
                    </label>
                    <select
                        id="department"
                        class="form-select"
                        v-model="form.department"
                        :class="{'is-invalid': departmentError}"
                    >
                        <option v-for="department in departments" :key="department.department_id" :value="department.department_id">
                            {{ department.department_name }}
                        </option>
                    </select>
                    <div v-if="departmentError" class="text-danger mt-1">{{ departmentError }}</div>
                </div>
                <div class="mb-3">
                    <label for="practice_start_date" class="form-label">
                        Practice Start Date <span class="text-danger">*</span>
                    </label>
                    <input
                        type="date"
                        id="practice_start_date"
                        class="form-control"
                        v-model="form.practice_start_date"
                        :class="{'is-invalid': practiceStartDateError}"
                    />
                    <div v-if="practiceStartDateError" class="text-danger mt-1">{{ practiceStartDateError }}</div>
                </div>
                <div class="mb-3">
                    <label for="fees" class="form-label">
                        Fees (₹) <span class="text-danger">*</span>
                    </label>
                    <input
                        type="text"
                        id="fees"
                        class="form-control"
                        v-model.trim="form.fees"
                        :class="{'is-invalid': feesError}"
                    />
                    <div v-if="feesError" class="text-danger mt-1">{{ feesError }}</div>
                </div>
                <div class="mb-3">
                    <label for="username" class="form-label">
                        Username <span class="text-danger">*</span>
                        <i
                            class="bi bi-info-circle ms-2 text-secondary"
                            data-bs-toggle="tooltip"
                            data-bs-html="true"
                            title="
                                <ul style='padding-left:1.2rem; margin:0;'>
                                    <li>Can be upto 25 characters long.</li>
                                    <li>Can include letters, underscores (_), and hyphens (-) only.</li>
                                </ul>
                            "
                            style="cursor:pointer;"
                        ></i>
                    </label>
                    <input
                        type="text"
                        id="username"
                        class="form-control"
                        v-model.trim="form.username"
                        :class="{'is-invalid': usernameError}"
                        autocomplete="username"
                    />
                    <div v-if="usernameError" class="text-danger mt-1">{{ usernameError }}</div>
                </div>
                <div class="mb-4">
                    <label for="password" class="form-label">
                        Password <span class="text-danger">*</span>
                        <i
                            class="bi bi-info-circle ms-2 text-secondary"
                            data-bs-toggle="tooltip"
                            data-bs-html="true"
                            title="
                                <ul style='padding-left:1.2rem; margin:0;'>
                                    <li>Must be at least 8 characters long.</li>
                                    <li>Must include at least one uppercase letter (A–Z).</li>
                                    <li>Must include at least one lowercase letter (a–z).</li>
                                    <li>Must include at least one number (0–9).</li>
                                    <li>Must include at least one special character (!, #, $, %, &).</li>
                                </ul>
                            "
                            style="cursor:pointer;"
                        ></i>
                    </label>
                    <div class="input-group">
                        <input
                            :type="showPassword ? 'text' : 'password'"
                            id="password"
                            class="form-control"
                            v-model.trim="form.password"
                            :class="{'is-invalid': passwordError}"
                            autocomplete="new-password"
                        />
                        <span
                            class="input-group-text password-eye"
                            @click="showPassword = !showPassword"
                            style="cursor:pointer;"
                        >
                            <i :class="showPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"></i>
                        </span>
                    </div>
                    <div v-if="passwordError" class="text-danger mt-1">{{ passwordError }}</div>
                </div>
                <div class="d-flex justify-content-between">
                    <router-link to="/admin/doctors" class="btn btn-outline-secondary w-50 me-2">Cancel</router-link>
                    <button type="submit" class="btn btn-primary w-50" :disabled="loading">
                        <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                        <span v-else>Create</span>
                    </button>
                </div>
            </form>
            <div v-if="errorMessage" class="text-danger text-center mt-2">{{ errorMessage }}</div>
        </div>
    </div>
</template>

<script>
    import axios from "axios";
    import { showToast } from "@/utils/toast.js";
    export default {
        name: "CreateDoctorForm",
        data() {
            return {
                loading: false,
                departments: [],
                showPassword: false,
                errorMessage: "",
                form: {
                    fullname: "",
                    email_name: "",
                    email_domain: "@example.com",
                    country_code: "+91",
                    phone_number: "",
                    qualifications: "",
                    license_number: "",
                    department: "",
                    practice_start_date: "",
                    fees: "",
                    username: "",
                    password: "",
                },
                fullnameError: "",
                emailError: "",
                phoneError: "",
                qualificationsError: "",
                licenseNumberError: "",
                departmentError: "",
                practiceStartDateError: "",
                feesError: "",
                usernameError: "",
                passwordError: "",
            };
        },
        watch: {
            "form.fullname"(value) {
                const regex = /^[A-Za-z.\s]{1,}$/;
                if (!value) this.fullnameError = "";
                else if (!regex.test(value)) this.fullnameError = "Please enter a valid Full Name.";
                else this.fullnameError = "";
            },
            "form.email_name"(value) {
                const regex = /^[A-Za-z0-9.]+$/;
                if (!value) this.emailError = "";
                else if (!regex.test(value)) this.emailError = "Please enter a valid Email.";
                else this.emailError = "";
            },
            "form.phone_number"(value) {
                const regex = /^[0-9]{1,10}$/;
                if (!value) this.phoneError = "";
                else if (!regex.test(value)) this.phoneError = "Please enter a valid Phone Number.";
                else this.phoneError = "";
            },
            "form.license_number"(value) {
                const regex = /^[A-Za-z0-9/-\s]{1,}$/;
                if (!value) this.licenseNumberError = "";
                else if (!regex.test(value)) this.licenseNumberError = "Please enter a valid License Number.";
                else this.licenseNumberError = "";
            },
            "form.fees"(value) {
                const regex = /^[0-9.]{1,}$/;
                if (!value) this.feesError = "";
                else if (!regex.test(value)) this.feesError = "Please enter a valid Fee.";
                else this.feesError = "";
            },
            "form.username"(value) {
                const regex = /^[A-Za-z0-9_-]{1,25}$/;
                if (!value) this.usernameError = "";
                else if (!regex.test(value)) this.usernameError = "Invalid Username. Please ensure it meets the requirements provided.";
                else this.usernameError = "";
            },
            "form.password"(value) {
                const regex = /^[A-Za-z0-9!#$%&]{1,}$/;
                if (!value) this.passwordError = "";
                else if (!regex.test(value)) this.passwordError = "Invalid Password. Please ensure it meets the requirements provided.";
                else this.passwordError = "";
            },
        },
        methods: {
            async createDoctor() {
                this.clearAllErrors();
                let valid = true;
                if (!this.form.fullname) {
                    this.fullnameError = "Full Name is required.";
                    valid = false;
                }
                if (!this.form.email_name) {
                    this.emailError = "Email is required.";
                    valid = false;
                }
                if (!this.form.phone_number) {
                    this.phoneError = "Phone Number is required.";
                    valid = false;
                }
                if (!this.form.qualifications) {
                    this.qualificationsError = "Qualifications are required.";
                    valid = false;
                }
                if (!this.form.license_number) {
                    this.licenseNumberError = "License Number is required.";
                    valid = false;
                }
                if (!this.form.department) {
                    this.departmentError = "Department is required.";
                    valid = false;
                }
                if (!this.form.practice_start_date) {
                    this.practiceStartDateError = "Practice Start Date is required.";
                    valid = false;
                }
                if (!this.form.fees) {
                    this.feesError = "Fees is required.";
                    valid = false;
                }
                if (!this.form.username) {
                    this.usernameError = "Username is required.";
                    valid = false;
                }
                if (!this.form.password) {
                    this.passwordError = "Password is required.";
                    valid = false;
                }
                if (this.form.fullname) {
                    if (this.form.fullname.length > 100) {
                        this.fullnameError = "Full Name can be upto 100 characters long.";
                        valid = false;
                    }
                }
                if (this.form.phone_number) {
                    if (this.form.phone_number.length !== 10) {
                        this.phoneError = "Please enter a valid Phone Number.";
                        valid = false;
                    }
                }
                if (this.form.license_number) {
                    if (this.form.license_number.length > 25) {
                        this.licenseNumberError = "License Number can be upto 25 characters long.";
                        valid = false;
                    }
                }
                if (this.form.practice_start_date) {
                    const practice_start_dateDate = new Date(this.form.practice_start_date);
                    const today = new Date();
                    if (practice_start_dateDate > today) {
                        this.practiceStartDateError = "Please enter a valid Practice Start Date.";
                        valid = false;
                    }
                }
                if (this.form.password) {
                    if (this.form.password.length < 8) {
                        this.passwordError = "Invalid Password. Please ensure it meets the requirements provided.";
                        valid = false;
                    }
                    const lower = /[a-z]/.test(this.form.password);
                    const upper = /[A-Z]/.test(this.form.password);
                    const number = /[0-9]/.test(this.form.password);
                    const special = /[!#$%&]/.test(this.form.password);
                    if (!(lower && upper && number && special)) {
                        this.passwordError = "Invalid Password. Please ensure it meets the requirements provided.";
                        valid = false;
                    }
                }
                if (!valid) return;
                try {
                    this.loading = true;
                    const payload = {
                        full_name: this.form.fullname,
                        email: this.form.email_name + this.form.email_domain,
                        phone_number: this.form.country_code + this.form.phone_number,
                        qualifications: this.form.qualifications,
                        license_number: this.form.license_number,
                        department_id: this.form.department,
                        practice_start_date: this.form.practice_start_date,
                        fees: this.form.fees,
                        username: this.form.username,
                        password: this.form.password,
                    };
                    const response = await axios.post('/admin/doctor', payload);
                    showToast(response.data.message,'success');
                    this.$router.push("/admin/doctors")
                } catch (err) {
                    if (err.response) {
                        this.errorMessage = err.response.data.message;
                    } else {
                        this.errorMessage = "Something went wrong. Please try again later.";
                    }
                } finally {
                    this.loading = false;
                }
            },
            async fetchDepartments() {
                const res = await axios.get("/admin/departments");
                this.departments = res.data.departments || [];
            },
            clearAllErrors() {
                this.errorMessage = "";
                this.fullnameError = "";
                this.emailError = "";
                this.phoneError = "";
                this.qualificationsError = "";
                this.licenseNumberError = "";
                this.departmentError = "";
                this.practiceStartDateError = "";
                this.feesError = "";
                this.usernameError = "";
                this.passwordError = "";
            },
        },
        mounted() {
            this.fetchDepartments();
            this.$nextTick(() => {
                if (window.bootstrap) {
                    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
                    tooltipTriggerList.forEach(el => {
                        new window.bootstrap.Tooltip(el, {trigger: 'hover', html: true, placement: 'top', boundary: 'window'});
                    });
                }
            });
        },
    };
</script>

<style scoped>
    .create-doctor-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .create-doctor-card {
        background-color: #e2e6ea;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.04);
        width: 100%;
        max-width: 600px;
    }
    .input-group .form-select.country-code {
        max-width: 75px;
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
    }
    .input-group .form-select.email-domain {
        max-width: 155px;
        border-top-left-radius: 0;
        border-bottom-left-radius: 0;
    }
    .form-control, .form-select {
        font-size: 0.95rem;
    }
</style>