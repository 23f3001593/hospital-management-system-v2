<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <PatientsTable :archived="false" title="Patients" :patients="patients" @patientsChanged="fetchPatients"/>
        <PatientsTable :archived="true" title="Archived Patients" :patients="archivedPatients"/>
    </div>
</template>

<script>
    import axios from "axios";
    import PatientsTable from "@/components/admin_components/patients-table.vue";
    export default {
        name: "PatientsOverview",
        components: { PatientsTable },
        data() {
            return {
                patients: [],
                archivedPatients: [],
                loading: false,
            };
        },
        methods: {
            async fetchPatients() {
                this.loading = true;
                const res = await axios.get("/admin/patients");
                this.patients = res.data.patients || [];
                this.archivedPatients = res.data.archived_patients || [];
                this.loading = false;
            },
        },
        mounted() {
            this.fetchPatients();
        },
    };
</script>