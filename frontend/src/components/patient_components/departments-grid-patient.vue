<template>
    <div class="container my-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="mb-0 fw-bold">{{ title }}</h2>
        </div>
        <div class="row">
            <div v-for="department in departments" :key="department.department_id" class="col-md-6 col-lg-4 mb-4">
                <router-link :to="{ name: 'DepartmentOverview', params: { id: department.department_id } }" class="btn card-btn">
                    <div class="card h-100">
                        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                            <h5 class="mb-0">{{ department.department_name }}</h5>                        
                        </div>
                        <div class="card-body">
                            <p class="mb-0">
                                <span class="description-text">{{ department.department_description }}</span>
                            </p>
                        </div>
                    </div>
                </router-link>
            </div>
            <div v-if="departments.length === 0" class="alert alert-dark text-center fst-italic col-12" role="alert">
                No departments found.
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "DepartmentsGridPatient",
        props: {
            title: String,
            departments: Array,
        },
    };
</script>

<style scoped>
    .description-text {
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.5;
        max-height: calc(1.5em * 5);
    }
    .card-btn {
        padding: 0;
        text-align: left;
        width: 100%;
    }
    .card-btn:focus, .card-btn:focus-visible, .card-btn:active {
        border-radius: 12px !important;
    }
</style>