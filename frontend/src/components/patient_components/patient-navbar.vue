<template>
    <div>
        <nav class="navbar navbar-expand-lg">
            <div class="container">
                <router-link to="/patient" class="navbar-brand">
                    <img src="@/assets/logo.png" alt="MediFlow" class="header-logo"/>
                </router-link>            
                <div class="ms-auto d-flex align-items-center">
                    <router-link to="/patient" class="btn me-3" :class="{'btn-primary':isActive('/patient'), 'btn-outline-primary':!isActive('/patient')}">
                        Home
                    </router-link>
                    <router-link to="/patient/treatments" class="btn me-3" :class="{'btn-primary':isActive('/patient/treatments'), 'btn-outline-primary':!isActive('/patient/treatments')}">
                        Treatments
                    </router-link>
                    <router-link to="/patient/history" class="btn me-3" :class="{'btn-primary':isActive('/patient/history'), 'btn-outline-primary':!isActive('/patient/history')}">
                        History
                    </router-link>
                    <div class="dropdown ms-3">
                        <a class="text-white d-flex align-items-center text-decoration-none dropdown-toggle" href="#" id="profileDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false" title="Profile">
                            <i class="bi bi-person-circle fs-4 me-2"></i>
                            <span class="d-none d-md-inline fw-medium">{{ currentUser.fullname }}</span>
                        </a>
                        <ul class="dropdown-menu dropdown-menu-start" aria-labelledby="profileDropdown">
                            <li>
                                <router-link class="dropdown-item dropdown-first" to="/patient/account">Account</router-link>
                            </li>
                            <li>
                                <button class="dropdown-item dropdown-last" @click="openLogoutModal">Logout</button>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </nav>
        <div v-if="showLogoutModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-md modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary">
                        <h4 class="modal-title fw-bold">Confirm Logout</h4>
                    </div>
                    <div class="modal-body">
                        <p class="mb-0">Are you sure you want to log out?</p>
                    </div>
                    <div class="modal-footer">
                        <div class="w-100">
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeLogoutModal">Cancel</button>
                                <button class="btn btn-danger w-50" @click="handleLogout" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                                    <span v-else>Logout</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { handleScrollLock } from "@/utils/scroll-lock";
    export default {
        name: "PatientNavbar",
        data() {
            return {
                showLogoutModal: false,
            };
        },
        computed: {
            currentUser() {
                return this.$store.state.user;
            },
        },
        watch: {
            showLogoutModal: 'updateScrollLock',
        },
        methods: {
            async handleLogout() {
                await this.$store.dispatch("logout")
                this.$router.push("/")
            },
            isActive(path) {
                return this.$route.path === path;
            },
            updateScrollLock() {
                handleScrollLock([this.showLogoutModal]);
            },
            openLogoutModal(department) {
                this.showLogoutModal = true;
            },
            closeLogoutModal() {
                this.showLogoutModal = false;
                this.$nextTick(() => {
                    handleScrollLock([this.showLogoutModal]);
                });
            },
        },
    };
</script>

<style scoped>
    .navbar {background-color: #1f2f7f;}
    .navbar .btn {font-weight: 500;}
    .header-logo {
        height: 48px;
        width: auto;
    }
    .dropdown-first {
        border-top-left-radius: 0.4rem !important;
        border-top-right-radius: 0.4rem !important;
    }
    .dropdown-last {
        border-bottom-left-radius: 0.4rem !important;
        border-bottom-right-radius: 0.4rem !important;
    }
</style>