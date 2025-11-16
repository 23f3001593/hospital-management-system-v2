<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <UpdateDoctorForm :doctor="doctor"/>
    </div>
</template>

<script>
    import axios from "axios";
    import UpdateDoctorForm from "@/components/doctor_components/update-doctor-form.vue";
    export default {
        name: "UpdateDoctor",
        components: { UpdateDoctorForm },
        data() {
            return {
                doctor: {},
                loading: false,
            };
        },
        methods: {
            async fetchDoctor() {
                this.loading = true;
                const id = this.$store.state.user.id;
                const res = await axios.get(`/doctor/${id}`);
                this.doctor = res.data;
                this.loading = false;
            },
        },
        mounted() {
            this.fetchDoctor();
        },
    };
</script>