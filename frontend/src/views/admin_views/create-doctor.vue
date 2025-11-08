<template>
    <div>
        <CreateDoctorForm/>
    </div>
</template>

<script>
    import CreateDoctorForm from "@/components/admin_components/create-doctor-form.vue";
    export default {
        name: "CreateDoctor",
        components: { CreateDoctorForm },
    };
</script>