<template>
    <div class="container py-5">
        <CreatePatientForm/>
    </div>
</template>

<script>
    import CreatePatientForm from "@/components/patient_components/create-patient-form.vue";
    export default {
        name: "CreatePatient",
        components: {
            CreatePatientForm,
        },
    };
</script>