<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <DepartmentDoctorsTable :department="department"/>
    </div>
</template>

<script>
    import axios from "axios";
    import DepartmentDoctorsTable from "@/components/patient_components/department-doctors-table.vue";
    export default {
        name: "DepartmentOverview",
        components: { DepartmentDoctorsTable },
        data() {
            return {
                department: {},
                loading: false,
            };
        },
        methods: {
            async fetchDepartment() {
                this.loading = true;
                const id = this.$route.params.id;
                const res = await axios.get(`/admin/department/${id}`);
                this.department = res.data;
                this.loading = false;
            },
        },
        mounted() {
            this.fetchDepartment();
        },
    };
</script>