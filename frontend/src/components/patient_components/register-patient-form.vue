<template>
  <div class="card shadow-sm mx-auto" style="max-width: 600px;">
    <div class="card-body">
      <h3 class="card-title text-center mb-4">Patient Registration</h3>
      <form @submit.prevent="registerPatient">

        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input v-model="form.full_name" type="text" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Date of Birth</label>
          <input v-model="form.dob" type="date" class="form-control" required />
        </div>

        <div class="mb-3">
            <label class="form-label d-block mb-1">Gender</label>
            <div class="form-check form-check-inline">
                <input
                class="form-check-input"
                type="radio"
                id="male"
                value="male"
                v-model="form.gender"
                required
                />
                <label class="form-check-label" for="male">Male</label>
            </div>
            <div class="form-check form-check-inline">
                <input
                class="form-check-input"
                type="radio"
                id="female"
                value="female"
                v-model="form.gender"
                required
                />
                <label class="form-check-label" for="female">Female</label>
            </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Phone Number (+91XXXXXXXXXX)</label>
          <input v-model="form.phone_number" type="text" class="form-control" required maxlength="13" />
        </div>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input v-model="form.email" type="email" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Address</label>
          <textarea v-model="form.address" class="form-control" required></textarea>
        </div>

        <div class="mb-3">
          <label class="form-label">Pincode</label>
          <input v-model="form.pincode" type="text" class="form-control" maxlength="6" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Username</label>
          <input v-model="form.username" type="text" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input v-model="form.password" type="password" class="form-control" required minlength="6" />
        </div>

        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm"></span>
          <span v-else>Register</span>
        </button>

        <p v-if="error" class="text-danger mt-3 text-center">{{ error }}</p>
        <p v-if="success" class="text-success mt-3 text-center">Registration successful!</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "RegisterPatientForm",
  data() {
    return {
      form: {
        full_name: "",
        username: "",
        email: "",
        phone_number: "+91",
        password: "",
        dob: "",
        gender: "",
        address: "",
        pincode: "",
      },
      loading: false,
      error: "",
      success: false,
    };
  },
  methods: {
    async registerPatient() {
      this.error = "";
      this.success = false;
      this.loading = true;

      try {
        const res = await axios.post("http://localhost:5000/api/patient/register", this.form);
        console.log(res.data);
        this.success = true;
        this.form = {
          full_name: "",
          username: "",
          email: "",
          phone_number: "+91",
          password: "",
          dob: "",
          gender: "",
          address: "",
          pincode: "",
        };
      } catch (err) {
        this.error = err.response?.data?.message || "Registration failed. Try again.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>