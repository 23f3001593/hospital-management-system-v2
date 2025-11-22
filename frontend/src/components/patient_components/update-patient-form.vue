<template>
    <div class="update-patient-container my-5">
        <div class="update-patient-card">
            <h1 class="text-center mb-4 text-primary fw-bold">Profile</h1>
            <form @submit.prevent="updatePatient">
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
                    <label for="dob" class="form-label">
                        Date of Birth
                    </label>
                    <input
                        type="date"
                        id="dob"
                        class="form-control"
                        v-model="form.dob"
                        disabled
                    />
                </div>
                <div class="mb-3">
                    <label for="gender" class="form-label">
                        Gender
                    </label>
                    <select
                        id="gender"
                        class="form-select"
                        v-model="form.gender"
                        disabled
                    >
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
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
                    <label for="address" class="form-label">
                        Address <span class="text-danger">*</span>
                    </label>
                    <textarea
                        id="address"
                        class="form-control"
                        v-model.trim="form.address"
                        :class="{'is-invalid': addressError}"
                        rows="4"
                        autocomplete="street-address"
                    ></textarea>
                    <div v-if="addressError" class="text-danger mt-1">{{ addressError }}</div>
                </div>
                <div class="mb-3">
                    <label for="pincode" class="form-label">
                        Pincode <span class="text-danger">*</span>
                    </label>
                    <input
                        type="text"
                        id="pincode"
                        class="form-control"
                        v-model.trim="form.pincode"
                        :class="{'is-invalid': pincodeError}"
                        maxlength="6"
                        autocomplete="postal-code"
                    />
                    <div v-if="pincodeError" class="text-danger mt-1">{{ pincodeError }}</div>
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
                    <router-link to="/patient" class="btn btn-outline-secondary w-50 me-2">Cancel</router-link>    
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
        name: "UpdatePatientForm",
        props: {
            patient: Object,
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
                    dob: "",
                    gender: "",
                    country_code: "",
                    phone_number: "",
                    email_name: "",
                    email_domain: "",
                    address: "",
                    pincode: "",
                    username: "",
                    current_password: "",
                    new_password: "",
                },
                fullnameError: "",
                phoneError: "",
                emailError: "",
                addressError: "",
                pincodeError: "",
                usernameError: "",
                currentPasswordError: "",
                newPasswordError: "",
            };
        },
        watch: {
            patient: {
                immediate: true,
                handler(newPatient) {
                    if (newPatient && Object.keys(newPatient).length > 0) {
                        this.form.fullname = newPatient.user.full_name || "";
                        this.form.dob = newPatient.dob || "";
                        this.form.gender = newPatient.gender || "";
                        if (newPatient.user.phone_number) {
                            const match = newPatient.user.phone_number.match(/^(\+\d{1,3}?)(\d{10})$/);
                            if (match) {
                                this.form.country_code = match[1];
                                this.form.phone_number = match[2];
                            }
                        }
                        if (newPatient.user.email) {
                            const [namePart, domainPart] = newPatient.user.email.split("@");
                            this.form.email_name = namePart || "";
                            this.form.email_domain = domainPart ? "@" + domainPart : "@example.com";
                        }
                        this.form.address = newPatient.address || "";
                        this.form.pincode = newPatient.pincode || "";
                        this.form.username = newPatient.user.username || "";
                        this.form.current_password = "";
                        this.form.new_password = "";
                    }
                },
            },
            showDeleteAccountModal: 'updateScrollLock',
            "form.fullname"(value) {
                const regex = /^[A-Za-z\s]{1,}$/;
                if (!value) this.fullnameError = "";
                else if (!regex.test(value)) this.fullnameError = "Please enter a valid Full Name.";
                else this.fullnameError = "";
            },
            "form.phone_number"(value) {
                const regex = /^[0-9]{1,10}$/;
                if (!value) this.phoneError = "";
                else if (!regex.test(value)) this.phoneError = "Please enter a valid Phone Number.";
                else this.phoneError = "";
            },
            "form.email_name"(value) {
                const regex = /^[A-Za-z0-9.]+$/;
                if (!value) this.emailError = "";
                else if (!regex.test(value)) this.emailError = "Please enter a valid Email.";
                else this.emailError = "";
            },
            "form.pincode"(value) {
                const regex = /^[0-9]{1,6}$/;
                if (!value) this.pincodeError = "";
                else if (!regex.test(value)) this.pincodeError = "Please enter a valid Pincode.";
                else this.pincodeError = "";
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
            async updatePatient() {
                this.clearAllErrors();
                let valid = true;
                if (!this.form.fullname) {
                    this.fullnameError = "Full Name is required.";
                    valid = false;
                }
                if (!this.form.phone_number) {
                    this.phoneError = "Phone Number is required.";
                    valid = false;
                }
                if (!this.form.email_name) {
                    this.emailError = "Email is required.";
                    valid = false;
                }
                if (!this.form.address) {
                    this.addressError = "Address is required.";
                    valid = false;
                }
                if (!this.form.pincode) {
                    this.pincodeError = "Pincode is required.";
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
                if (this.form.pincode) {
                    if (this.form.pincode.length !== 6) {
                        this.pincodeError = "Please enter a valid Pincode.";
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
                    formData.append('phone_number', this.form.country_code + this.form.phone_number);
                    formData.append('email', this.form.email_name + this.form.email_domain);
                    formData.append('address', this.form.address);
                    formData.append('pincode', this.form.pincode);
                    formData.append('username', this.form.username);
                    formData.append('current_password', this.form.current_password);
                    formData.append('new_password', this.form.new_password);
                    const response = await axios.put(`/patient/${id}`, formData, {headers: {'Content-Type': 'multipart/form-data'}});
                    showToast(response.data.message,'success');
                    this.$store.commit('setUser', {
                        id: this.$store.state.user.id,
                        role: this.$store.state.user.role,
                        fullname: this.form.fullname
                    });
                    localStorage.setItem('user_fullname', this.form.fullname);
                    this.$router.push("/patient")
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
                    await axios.patch(`/patient/${id}`);
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
            openDeleteAccountModal(patient) {
                this.showDeleteAccountModal = true;
            },
            closeDeleteAccountModal() {
                this.showDeleteAccountModal = false;
                this.deleteErrorMessage = "";
            },
            clearAllErrors() {
                updateErrorMessage: "",
                this.fullnameError = "";
                this.phoneError = "";
                this.emailError = "";
                this.addressError = "";
                this.pincodeError = "";
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
    .update-patient-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .update-patient-card {
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