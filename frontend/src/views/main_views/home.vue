<template>
    <div class="d-flex flex-column min-vh-100">
        <HomeNavbar/>
        <router-view class="flex-grow-1"/>
        <Footer/>
        <Toast/>
    </div>
</template>

<script>
    import HomeNavbar from "@/components/main_components/home-navbar.vue";
    import Footer from "@/components/main_components/footer.vue";
    import Toast from "@/components/main_components/toast.vue";
    export default {
        name: "Home",
        components: { HomeNavbar, Footer, Toast },
    }
</script>