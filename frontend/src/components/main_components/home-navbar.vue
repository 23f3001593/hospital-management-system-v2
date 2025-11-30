<template>
    <div>
        <nav class="navbar navbar-expand-lg">
            <div class="container">
                <router-link to="/" class="navbar-brand">
                    <img src="@/assets/logo.png" alt="MediFlow" class="header-logo"/>
                </router-link>            
                <div class="ms-auto d-flex align-items-center">
                    <router-link to="/login" class="btn" :class="{'btn-primary':isActive('/login'), 'btn-outline-primary':!isActive('/login')}">
                        Login
                    </router-link>
                </div>
            </div>
        </nav>
    </div>
</template>

<script>
    export default {
        name: "HomeNavbar",
        methods: {
            isActive(path) {
                return this.$route.path === path;
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
</style>