<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <AvailabilityTable title="Next Week’s Availability" :availability="availability" @availabilityChanged="fetchAvailability"/>
    </div>
</template>

<script>
    import axios from "axios";
    import AvailabilityTable from "@/components/doctor_components/availability-table.vue";
    export default {
        name: "Availability",
        components: { AvailabilityTable },
        data() {
            return {
                availability: [],
                loading: false,
            };
        },
        methods: {
            async fetchAvailability() {
                this.loading = true;
                const id = this.$store.state.user.id;
                const res = await axios.get(`/doctor/availability/${id}`);
                this.availability = res.data;
                this.loading = false;
            },
        },
        mounted() {
            this.fetchAvailability();
        },
    }
</script>