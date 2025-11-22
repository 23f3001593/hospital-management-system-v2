<template>
    <div class="container my-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="mb-0 fw-bold">{{ title }}</h2>
        </div>
        <div v-for="treatment in treatments" :key="treatment.treatment_id" class="mb-4">
            <div class="card h-100">
                <div class="card-body">
                    <div class="row mb-4 text-center">
                        <div class="col-4 text-start"><h5>{{ treatment.doctor.user.full_name }}</h5></div>
                        <div class="col-4"><h5>Department of {{ treatment.doctor.department.department_name }}</h5></div>
                        <div class="col-4 text-end"><h5>{{ formatDate(treatment.appointment.appointment_date) }}</h5></div>
                    </div>
                    <p class="mb-2"><strong>Tests:</strong> {{ treatment.tests }}</p>
                    <p class="mb-2"><strong>Diagnosis:</strong> {{ treatment.diagnosis }}</p>
                    <p class="mb-2"><strong>Prescription:</strong> {{ treatment.prescription }}</p>
                    <p class="mb-2"><strong>Medicines:</strong> {{ treatment.medicines }}</p>
                    <p class="mb-0"><strong>Notes:</strong> {{ treatment.notes }}</p>
                </div>
            </div>
        </div>
        <div v-if="treatments.length === 0" class="alert alert-dark text-center fst-italic" role="alert">
            No treatments found.
        </div>
    </div>
</template>

<script>
    export default {
        name: "TreatmentsGrid",
        props: {
            title: String,
            treatments: Array,
        },
        methods: {
            formatDate(appointment_date) {
                if (!appointment_date) return "";
                const date = new Date(appointment_date);
                const options = { day: '2-digit', month: 'long', year: 'numeric' };
                return date.toLocaleDateString('en-GB', options);
            },
        },
    };
</script>