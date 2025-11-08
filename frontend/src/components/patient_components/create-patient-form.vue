<template>
    <div class="register-container my-5">
        <div class="register-card">
            <h1 class="text-center mb-4 text-primary fw-bold">Sign Up</h1>
            <form @submit.prevent="registerPatient">
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
                        Date of Birth <span class="text-danger">*</span>
                    </label>
                    <input
                        type="date"
                        id="dob"
                        class="form-control"
                        v-model="form.dob"
                        :class="{'is-invalid': dobError}"
                        autocomplete="bday"
                    />
                    <div v-if="dobError" class="text-danger mt-1">{{ dobError }}</div>
                </div>
                <div class="mb-3">
                    <label for="gender" class="form-label">
                        Gender <span class="text-danger">*</span>
                    </label>
                    <select
                        id="gender"
                        class="form-select"
                        v-model="form.gender"
                        :class="{'is-invalid': genderError}"
                        autocomplete="sex"
                    >
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                    <div v-if="genderError" class="text-danger mt-1">{{ genderError }}</div>
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
                <div class="d-grid">
                    <button type="submit" class="btn btn-primary justify-content-center align-items-center" :disabled="loading">
                        <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                        <span v-else>Register</span>
                    </button>
                </div>
            </form>
            <p class="text-center mt-3">
                Already have an account?
                <router-link to="/login" class="text-decoration-none text-primary fw-medium">Login</router-link>
            </p>
            <div v-if="errorMessage" class="text-danger text-center mt-2">{{ errorMessage }}</div>
        </div>
    </div>
</template>

<script>
    import axios from "axios"
    export default {
        name: "CreatePatientForm",
        data() {
            return {
                loading: false,
                showPassword: false,
                errorMessage: "",
                form: {
                    fullname: "",
                    dob: "",
                    gender: "",
                    country_code: "+91",
                    phone_number: "",
                    email_name: "",
                    email_domain: "@example.com",
                    address: "",
                    pincode: "",
                    username: "",
                    password: "",
                },
                fullnameError: "",
                dobError: "",
                genderError: "",
                phoneError: "",
                emailError: "",
                addressError: "",
                pincodeError: "",
                usernameError: "",
                passwordError: "",
            };
        },
        watch: {
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
            "form.password"(value) {
                const regex = /^[A-Za-z0-9!#$%&]{1,}$/;
                if (!value) this.passwordError = "";
                else if (!regex.test(value)) this.passwordError = "Invalid Password. Please ensure it meets the requirements provided.";
                else this.passwordError = "";
            },
        },
        methods: {
            async registerPatient() {
                this.clearAllErrors();
                let valid = true;
                if (!this.form.fullname) {
                    this.fullnameError = "Full Name is required.";
                    valid = false;
                }
                if (!this.form.dob) {
                    this.dobError = "Date of Birth is required.";
                    valid = false;
                }
                if (!this.form.gender) {
                    this.genderError = "Gender is required.";
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
                if (this.form.pincode) {
                    if (this.form.pincode.length !== 6) {
                        this.pincodeError = "Please enter a valid Pincode.";
                        valid = false;
                    }
                }
                if (this.form.dob) {
                    const dobDate = new Date(this.form.dob);
                    const today = new Date();
                    if (dobDate > today) {
                        this.dobError = "Please enter a valid Date of Birth.";
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
                        dob: this.form.dob,
                        gender: this.form.gender,
                        phone_number: this.form.country_code + this.form.phone_number,
                        email: this.form.email_name + this.form.email_domain,
                        address: this.form.address,
                        pincode: this.form.pincode,
                        username: this.form.username,
                        password: this.form.password,
                    };
                    const response = await axios.post('/patient', payload);
                } catch (error) {
                    if (error.response) {
                        this.errorMessage = error.response.data.message;
                    } else if (error.request) {
                        this.errorMessage = "Failed to reach server. Please try again later.";
                    } else {
                        this.errorMessage = "Something went wrong. Please try again later.";
                    }
                } finally {
                    this.loading = false;
                }
            },
            clearAllErrors() {
                this.errorMessage = "";
                this.fullnameError = "";
                this.dobError = "";
                this.genderError = "";
                this.phoneError = "";
                this.emailError = "";
                this.addressError = "";
                this.pincodeError = "";
                this.usernameError = "";
                this.passwordError = "";
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
    .register-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .register-card {
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