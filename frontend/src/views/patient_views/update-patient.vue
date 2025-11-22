<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <UpdatePatientForm :patient="patient"/>
    </div>
</template>

<script>
    import axios from "axios";
    import UpdatePatientForm from "@/components/patient_components/update-patient-form.vue";
    export default {
        name: "UpdatePatient",
        components: { UpdatePatientForm },
        data() {
            return {
                patient: {},
                loading: false,
            };
        },
        methods: {
            async fetchPatient() {
                this.loading = true;
                const id = this.$store.state.user.id;
                const res = await axios.get(`/patient/${id}`);
                this.patient = res.data;
                this.loading = false;
            },
        },
        mounted() {
            this.fetchPatient();
        },
    };
</script>