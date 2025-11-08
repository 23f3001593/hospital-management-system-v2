<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <DepartmentsGrid :archived="false" title="Departments" :departments="departments" @departmentsChanged="fetchDepartments"/>
        <DepartmentsGrid :archived="true" title="Archived Departments" :departments="archivedDepartments"/>
    </div>
</template>

<script>
    import axios from "axios";
    import DepartmentsGrid from "@/components/admin_components/departments-grid.vue";
    export default {
        name: "DepartmentsOverview",
        components: { DepartmentsGrid },
        data() {
            return {
                departments: [],
                archivedDepartments: [],
                loading: false,
            };
        },
        methods: {
            async fetchDepartments() {
                this.loading = true;
                const res = await axios.get("/admin/departments");
                this.departments = res.data.departments || [];
                this.archivedDepartments = res.data.archived_departments || [];
                this.loading = false;
            },
        },
        mounted() {
            this.fetchDepartments();
        },
    };
</script>