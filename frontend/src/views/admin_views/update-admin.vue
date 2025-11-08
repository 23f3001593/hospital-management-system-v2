<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height:80vh;">
        <div class="spinner-grow" role="status"></div>
    </div>
    <div v-else>
        <UpdateAdminForm :admin="admin"/>
    </div>
</template>

<script>
    import axios from "axios";
    import UpdateAdminForm from "@/components/admin_components/update-admin-form.vue";
    export default {
        name: "UpdateAdmin",
        components: { UpdateAdminForm },
        data() {
            return {
                admin: {},
                loading: false,
            };
        },
        methods: {
            async fetchAdmin() {
                this.loading = true;
                const res = await axios.get("/admin");
                this.admin = res.data;
                this.loading = false;
            },
        },
        mounted() {
            this.fetchAdmin();
        },
    };
</script>