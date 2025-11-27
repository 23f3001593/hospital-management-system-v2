<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <TreatmentsGrid title="Treatments History" :treatments="treatments"/>
    </div>
</template>

<script>
    import axios from "axios";
    import TreatmentsGrid from "@/components/patient_components/treatments-grid.vue";
    export default {
        name: "TreatmentsOverview",
        components: { TreatmentsGrid },
        data() {
            return {
                treatments: [],
                loading: false,
            };
        },
        methods: {
            async fetchTreatments() {
                this.loading = true;
                const id = this.$store.state.user.id;
                const response = await axios.get(`/patient/treatments/${id}`);
                this.treatments = response.data.treatments;
                this.treatments.sort((a, b) => {
                    return new Date(b.appointment.appointment_date) - new Date(a.appointment.appointment_date);
                });
                this.loading = false;
            },
        },
        mounted() {
            this.fetchTreatments();
        },
    };
</script>