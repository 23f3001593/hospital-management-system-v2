<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <AdminStatsGrid title="Quick Stats" :stats="stats"/>
    </div>
</template>

<script>
    import axios from "axios";
    import AdminStatsGrid from "@/components/admin_components/admin-stats-grid.vue";
    export default {
        name: "AdminHome",
        components: { AdminStatsGrid },
        data() {
            return {
                stats: {},
                loading: false,
            };
        },
        methods: {
            async fetchStats() {
                this.loading = true;
                const response = await axios.get("/admin/summary");
                this.stats = response.data
                this.loading = false;
            },
        },
        mounted() {
            this.fetchStats();
        },
    };
</script>