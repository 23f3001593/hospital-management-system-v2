<template>
    <div class="d-flex flex-column min-vh-100">
        <PatientNavbar/>
        <router-view class="flex-grow-1"/>
        <Footer/>
        <Toast/>
    </div>
</template>

<script>
    import PatientNavbar from "@/components/patient_components/patient-navbar.vue";
    import Footer from "@/components/main_components/footer.vue";
    import Toast from "@/components/main_components/toast.vue";
    export default {
        name: "PatientDashboard",
        components: { PatientNavbar, Footer, Toast },
    }
</script>