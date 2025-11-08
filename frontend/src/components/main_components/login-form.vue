<template>
    <div class="login-container">
        <div class="login-card">
            <h1 class="text-center mb-4 text-primary fw-bold">Login</h1>
            <form @submit.prevent="handleLogin">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input
                        type="text"
                        id="username"
                        class="form-control"
                        v-model.trim="username"
                        :class="{'is-invalid': usernameError}"
                        autocomplete="username"
                    />
                    <div v-if="usernameError" class="text-danger mt-1">{{ usernameError }}</div>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <div class="input-group">
                        <input
                            :type="showPassword ? 'text' : 'password'"
                            id="password"
                            class="form-control"
                            v-model.trim="password"
                            :class="{'is-invalid': passwordError}"
                            autocomplete="current-password"
                        />
                        <span class="input-group-text password-eye" @click="showPassword = !showPassword" style="cursor:pointer;">
                            <i :class="showPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"></i>
                        </span>
                    </div>
                    <div v-if="passwordError" class="text-danger mt-1">{{ passwordError }}</div>
                </div>
                <div class="d-grid">
                    <button type="submit" class="btn btn-primary justify-content-center align-items-center" :disabled="loading">
                        <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                        <span v-else>Login</span>
                    </button>
                </div>
            </form>
            <p class="text-center mt-3">
                Don't have an account?
                <router-link to="/register" class="text-decoration-none text-primary fw-medium">Create</router-link>
            </p>
            <div v-if="errorMessage" class="text-danger text-center mt-2">{{ errorMessage }}</div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "LoginForm",
        data() {
            return {
                username: "",
                password: "",
                usernameError: "",
                passwordError: "",
                errorMessage: "",
                loading: false,
                showPassword: false,
            };
        },
        methods: {
            async handleLogin() {
                this.usernameError = "";
                this.passwordError = "";
                this.errorMessage = "";
                const usernamePattern = /^[a-zA-Z0-9_-]{1,25}$/;
                const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!#$%&])(?!.*\s).{8,}$/;
                if (!this.username) {this.usernameError = "Username is required.";}
                if (!this.password) {this.passwordError = "Password is required.";}
                if (this.usernameError || this.passwordError) {return;}
                if (!usernamePattern.test(this.username) || !passwordPattern.test(this.password)) {
                    this.errorMessage = "Invalid username or password.";
                    return;
                }
                this.loading = true;
                try {
                    await this.$store.dispatch("login", {
                        username: this.username,
                        password: this.password
                    })
                    const role = this.$store.state.user.role
                    if (role === "admin") {
                        this.$router.push("/admin")
                    } else if (role === "doctor") {
                        this.$router.push("/doctor")
                    } else if (role === "patient") {
                        this.$router.push("/patient")
                    } else {
                        this.$router.push("/")
                    }
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
        },
    };
</script>

<style scoped>
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    .login-card {
        background-color: #e2e6ea;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.04);
        width: 100%;
        max-width: 400px;
    }
</style>