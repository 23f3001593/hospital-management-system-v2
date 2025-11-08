<template>
    <div class="d-flex flex-column min-vh-100">
        <AdminNavbar/>
        <router-view class="flex-grow-1"/>
        <Footer/>
        <Toast/>
    </div>
</template>

<script>
    import AdminNavbar from "@/components/admin_components/admin-navbar.vue"
    import Footer from "@/components/main_components/footer.vue"
    import Toast from "@/components/main_components/toast.vue"
    export default {
        name: "AdminDashboard",
        components: { AdminNavbar, Footer, Toast },
    }
</script>