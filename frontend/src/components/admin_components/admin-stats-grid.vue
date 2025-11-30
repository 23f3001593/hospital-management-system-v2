<template>
    <div class="container my-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="mb-0 fw-bold">{{ title }}</h2>
        </div>
        <div class="row">
            <div v-for="(value,key) in stats" :key="key" class="col-md-6 col-lg-4 mb-4">
                <router-link :to="getStatConfig(key,value).route" class="btn card-btn">
                    <div class="card h-100">
                        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                            <h5 class="mb-0">{{ getStatConfig(key,value).title }}</h5>                        
                        </div>
                        <div class="card-body">
                            <p class="mb-0">{{ getStatConfig(key,value).description }}</p>
                        </div>
                    </div>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "AdminStatsGrid",
        props: {
            title: String,
            stats: Object,
        },
        methods: {
            getStatConfig(key, value) {
                const config = {
                    doctor_count: {
                        title: "Doctors",
                        description: `Total number of active registered doctors: ${value}`,
                        route: "/admin/doctors",
                    },
                    patient_count: {
                        title: "Patients",
                        description: `Total number of active registered patients: ${value}`,
                        route: "/admin/patients",
                    },
                    appointment_count: {
                        title: "Appointments",
                        description: `Total number of scheduled appointments: ${value}`,
                        route: "/admin/appointments",
                    },
                };
                return config[key];
            },
        },
    };
</script>

<style scoped>
    .card-btn {
        padding: 0;
        text-align: left;
        width: 100%;
    }
    .card-btn:focus, .card-btn:focus-visible, .card-btn:active {
        border-radius: 12px !important;
    }
</style>