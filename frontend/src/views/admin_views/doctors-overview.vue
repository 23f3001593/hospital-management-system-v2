<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <DoctorsTable :archived="false" title="Doctors" :doctors="doctors" @doctorsChanged="fetchDoctors"/>
        <DoctorsTable :archived="true" title="Archived Doctors" :doctors="archivedDoctors"/>
    </div>
</template>

<script>
    import axios from "axios";
    import DoctorsTable from "@/components/admin_components/doctors-table.vue";
    export default {
        name: "DoctorsOverview",
        components: { DoctorsTable },
        data() {
            return {
                doctors: [],
                archivedDoctors: [],
                loading: false,
            };
        },
        methods: {
            async fetchDoctors() {
                this.loading = true;
                const res = await axios.get("/admin/doctors");
                this.doctors = res.data.doctors || [];
                this.archivedDoctors = res.data.archived_doctors || [];
                this.loading = false;
            },
        },
        mounted() {
            this.fetchDoctors();
        },
    };
</script>