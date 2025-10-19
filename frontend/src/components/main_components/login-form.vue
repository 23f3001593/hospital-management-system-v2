<template>
  <div class="login-container">
    <div class="card p-4 shadow-sm" style="width: 350px;">
      <h3 class="text-center mb-4">Login</h3>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="username" type="text" id="username" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" id="password" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
        <div v-if="errorMessage" class="text-danger mt-3 text-center">
          {{ errorMessage }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
    import axios from "axios";
    export default {
        name: "LoginForm",
        data() {
            return {
                username: "",
                password: "",
                errorMessage: "",
            };
        },
        methods: {
            async handleLogin() {
                try {
                    await this.$store.dispatch("login", {
                        username: this.username,
                        password: this.password
                    })
                    // this.$router.push("/");
                    this.errorMessage = "Login successfull !"
                } catch (error) {
                    // Handle backend or network errors
                    if (error.response) {
                        // Server responded with a non-2xx status
                        this.errorMessage = error.response.data.message;
                    } else if (error.request) {
                        // No response from server
                        this.errorMessage = "No response from server";
                    } else {
                        // Other errors
                        this.errorMessage = "Error connecting to server";
                    }
                    console.error("Login error:", error);
                }
            },
        },
    };
</script>

<style scoped>
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh; /* Full viewport height */
        margin: 0;
        padding: 0;
    }
    .card {
        border-radius: 12px;
    }
</style>