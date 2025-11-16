<template>
    <div class="d-flex flex-column min-vh-100">
        <DoctorNavbar/>
        <router-view class="flex-grow-1"/>
        <Footer/>
        <Toast/>
    </div>
</template>

<script>
    import DoctorNavbar from "@/components/doctor_components/doctor-navbar.vue";
    import Footer from "@/components/main_components/footer.vue";
    import Toast from "@/components/main_components/toast.vue";
    export default {
        name: "DoctorDashboard",
        components: { DoctorNavbar, Footer, Toast },
    }
</script>