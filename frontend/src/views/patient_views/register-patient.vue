<template>
  <div class="container py-5">
    <RegisterPatientForm />
  </div>
</template>

<script>
import RegisterPatientForm from "@/components/patient_components/register-patient-form.vue";

export default {
  name: "RegisterPatient",
  components: {
    RegisterPatientForm,
  },
};
</script>