<template>
    <div class="update-doctor-container my-5">
        <div class="update-doctor-card">
            <h1 class="text-center mb-4 text-primary fw-bold">Profile</h1>
            <form @submit.prevent="updateDoctor">
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
                        License Number
                    </label>
                    <input
                        type="text"
                        id="license_number"
                        class="form-control"
                        v-model.trim="form.license_number"
                        disabled
                    />
                </div>
                <div class="mb-3">
                    <label for="department" class="form-label">
                        Department
                    </label>
                    <input
                        type="text"
                        id="department"
                        class="form-control"
                        v-model.trim="form.department"
                        disabled
                    />
                </div>
                <div class="mb-3">
                    <label for="practice_start_date" class="form-label">
                        Practice Start Date
                    </label>
                    <input
                        type="date"
                        id="practice_start_date"
                        class="form-control"
                        v-model="form.practice_start_date"
                        disabled
                    />
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
                    <label for="current_password" class="form-label">
                        Current Password <span class="text-danger">*</span>
                    </label>
                    <div class="input-group">
                        <input
                            :type="showCurrentPassword ? 'text' : 'password'"
                            id="current_password"
                            class="form-control"
                            v-model.trim="form.current_password"
                            :class="{'is-invalid': currentPasswordError}"
                            autocomplete="current-password"
                        />
                        <span
                            class="input-group-text password-eye"
                            @click="showCurrentPassword = !showCurrentPassword"
                            style="cursor:pointer;"
                        >
                            <i :class="showCurrentPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"></i>
                        </span>
                    </div>
                    <div v-if="currentPasswordError" class="text-danger mt-1">{{ currentPasswordError }}</div>
                </div>
                <div class="mb-4">
                    <label for="new_password" class="form-label">
                        New Password
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
                            :type="showNewPassword ? 'text' : 'password'"
                            id="new_password"
                            class="form-control"
                            v-model.trim="form.new_password"
                            :class="{'is-invalid': newPasswordError}"
                            autocomplete="new-password"
                        />
                        <span
                            class="input-group-text password-eye"
                            @click="showNewPassword = !showNewPassword"
                            style="cursor:pointer;"
                        >
                            <i :class="showNewPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"></i>
                        </span>
                    </div>
                    <div v-if="newPasswordError" class="text-danger mt-1">{{ newPasswordError }}</div>
                </div>
                <div class="d-flex justify-content-between mb-2">
                    <router-link to="/doctor" class="btn btn-outline-secondary w-50 me-2">Cancel</router-link>    
                    <button type="submit" class="btn btn-primary w-50" :disabled="updateLoading || deleteLoading">
                        <span v-if="updateLoading" class="spinner-border spinner-border-sm" role="status"></span>
                        <span v-else>Update</span>
                    </button>
                </div>
                <div class="d-flex justify-content-between">
                    <button type="button" class="btn btn-danger w-100" @click="openDeleteAccountModal" :disabled="deleteLoading || updateLoading">Delete Account</button>
                </div>
            </form>
            <div v-if="updateErrorMessage" class="text-danger text-center mt-2">{{ updateErrorMessage }}</div>
        </div>
        <div v-if="showDeleteAccountModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-md modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary">
                        <h4 class="modal-title fw-bold">Confirm Account Deletion</h4>
                    </div>
                    <div class="modal-body">
                        <p class="mb-0">Are you sure you want to delete your account?</p>
                    </div>
                    <div class="modal-footer">
                        <div class="w-100">
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeDeleteAccountModal">Cancel</button>
                                <button class="btn btn-danger w-50" @click="deleteAccount()" :disabled="deleteLoading">
                                    <span v-if="deleteLoading" class="spinner-border spinner-border-sm" role="status"></span>
                                    <span v-else>Delete</span>
                                </button>
                            </div>
                            <div v-if="deleteErrorMessage" class="text-danger text-center mt-2">{{ deleteErrorMessage }}</div>
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
        name: "UpdateDoctorForm",
        props: {
            doctor: Object,
        },
        data() {
            return {
                updateLoading: false,
                deleteLoading: false,
                showCurrentPassword: false,
                showNewPassword: false,
                showDeleteAccountModal: false,
                updateErrorMessage: "",
                deleteErrorMessage: "",
                form: {
                    fullname: "",
                    email_name: "",
                    email_domain: "",
                    country_code: "",
                    phone_number: "",
                    qualifications: "",
                    license_number: "",
                    department: "",
                    practice_start_date: "",
                    fees: "",
                    username: "",
                    current_password: "",
                    new_password: "",
                },
                fullnameError: "",
                emailError: "",
                phoneError: "",
                qualificationsError: "",
                feesError: "",
                usernameError: "",
                currentPasswordError: "",
                newPasswordError: "",
            };
        },
        watch: {
            doctor: {
                immediate: true,
                handler(newDoctor) {
                    if (newDoctor && Object.keys(newDoctor).length > 0) {
                        this.form.fullname = newDoctor.user.full_name || "";
                        if (newDoctor.user.email) {
                            const [namePart, domainPart] = newDoctor.user.email.split("@");
                            this.form.email_name = namePart || "";
                            this.form.email_domain = domainPart ? "@" + domainPart : "@example.com";
                        }
                        if (newDoctor.user.phone_number) {
                            const match = newDoctor.user.phone_number.match(/^(\+\d{1,3}?)(\d{10})$/);
                            if (match) {
                                this.form.country_code = match[1];
                                this.form.phone_number = match[2];
                            }
                        }
                        this.form.qualifications = newDoctor.qualifications || "";
                        this.form.license_number = newDoctor.license_number || "";
                        this.form.department = newDoctor.department.department_name || "";
                        this.form.practice_start_date = newDoctor.practice_start_date || "";
                        if (newDoctor.fees) {
                            const formatedFees = parseFloat(newDoctor.fees).toFixed(2);
                            this.form.fees = formatedFees || "";
                        }
                        this.form.username = newDoctor.user.username || "";
                        this.form.current_password = "";
                        this.form.new_password = "";
                    }
                },
            },
            showDeleteAccountModal: 'updateScrollLock',
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
            "form.current_password"(value) {
                if (!value) this.currentPasswordError = "";
                else this.currentPasswordError = "";
            },
            "form.new_password"(value) {
                const regex = /^[A-Za-z0-9!#$%&]{0,}$/;
                if (!value) this.newPasswordError = "";
                else if (!regex.test(value)) this.newPasswordError = "Invalid Password. Please ensure it meets the requirements provided.";
                else this.newPasswordError = "";
            },
        },
        methods: {
            async updateDoctor() {
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
                if (!this.form.fees) {
                    this.feesError = "Fees is required.";
                    valid = false;
                }
                if (!this.form.username) {
                    this.usernameError = "Username is required.";
                    valid = false;
                }
                if (!this.form.current_password) {
                    this.currentPasswordError = "Current Password is required.";
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
                if (this.form.current_password) {
                    if (this.form.current_password.length < 8) {
                        this.currentPasswordError = "Invalid Password.";
                        valid = false;
                    }
                    const lower = /[a-z]/.test(this.form.current_password);
                    const upper = /[A-Z]/.test(this.form.current_password);
                    const number = /[0-9]/.test(this.form.current_password);
                    const special = /[!#$%&]/.test(this.form.current_password);
                    if (!(lower && upper && number && special)) {
                        this.currentPasswordError = "Invalid Password.";
                        valid = false;
                    }
                }
                if (this.form.new_password) {
                    if (this.form.new_password.length < 8) {
                        this.newPasswordError = "Invalid Password. Please ensure it meets the requirements provided.";
                        valid = false;
                    }
                    const lower = /[a-z]/.test(this.form.new_password);
                    const upper = /[A-Z]/.test(this.form.new_password);
                    const number = /[0-9]/.test(this.form.new_password);
                    const special = /[!#$%&]/.test(this.form.new_password);
                    if (!(lower && upper && number && special)) {
                        this.newPasswordError = "Invalid Password. Please ensure it meets the requirements provided.";
                        valid = false;
                    }
                }
                if (!valid) return;
                try {
                    this.updateLoading = true;
                    const id = this.$store.state.user.id;
                    const formData = new FormData();
                    formData.append('full_name', this.form.fullname);
                    formData.append('email', this.form.email_name + this.form.email_domain);
                    formData.append('phone_number', this.form.country_code + this.form.phone_number);
                    formData.append('qualifications', this.form.qualifications);
                    formData.append('fees', this.form.fees);
                    formData.append('username', this.form.username);
                    formData.append('current_password', this.form.current_password);
                    formData.append('new_password', this.form.new_password);
                    const response = await axios.put(`/doctor/${id}`, formData, {headers: {'Content-Type': 'multipart/form-data'}});
                    showToast(response.data.message,'success');
                    this.$store.commit('setUser', {
                        id: this.$store.state.user.id,
                        role: this.$store.state.user.role,
                        fullname: this.form.fullname
                    });
                    localStorage.setItem('user_fullname', this.form.fullname);
                    this.$router.push("/doctor")
                } catch (err) {
                    if (err.response) {
                        this.updateErrorMessage = err.response.data.message;
                    } else {
                        this.updateErrorMessage = "Something went wrong. Please try again later.";
                    }
                } finally {
                    this.updateLoading = false;
                }
            },
            async deleteAccount() {
                this.deleteErrorMessage = "";
                try {
                    this.deleteLoading = true;
                    const id = this.$store.state.user.id;
                    await axios.patch(`/doctor/${id}`);
                    this.closeDeleteAccountModal();
                    await this.$store.dispatch("logout")
                    this.$router.push("/")
                } catch (error) {
                    if (error.response) {
                        this.deleteErrorMessage = error.response.data.message;
                    } else {
                        this.deleteErrorMessage = "Something went wrong. Please try again later.";
                    }
                } finally {
                    this.deleteLoading = false;
                }
            },
            updateScrollLock() {
                handleScrollLock([this.showDeleteAccountModal]);
            },
            openDeleteAccountModal(doctor) {
                this.showDeleteAccountModal = true;
            },
            closeDeleteAccountModal() {
                this.showDeleteAccountModal = false;
                this.deleteErrorMessage = "";
            },
            clearAllErrors() {
                updateErrorMessage: "",
                this.fullnameError = "";
                this.emailError = "";
                this.phoneError = "";
                this.qualificationsError = "";
                this.feesError = "";
                this.usernameError = "";
                this.currentPasswordError = "";
                this.newPasswordError = "";
            },
        },
        mounted() {
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
    .update-doctor-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .update-doctor-card {
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
    .modal-header .btn-close {
        filter: invert(1) brightness(200%);
        opacity: 1;
    }
    .modal-header .btn-close:focus, .modal-header .btn-close:active {
        box-shadow: none !important;
    }
</style>