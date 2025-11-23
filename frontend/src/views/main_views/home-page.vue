<template>
    <div>
        <div class="container intro-text text-center py-5">
            <h1 class="text-primary fw-bold">Welcome to MediFlow</h1>
            <p class="lead text-secondary">A Simplified and Modern Hospital Experience</p>
            <div class="row justify-content-center mt-4">
                <div class="col-md-9">
                    <p class="text-muted fs-5">
                        <strong>MediFlow</strong> represents a modern approach to healthcare where hospital services, patient interactions, and medical information move smoothly and efficiently across the system. By eliminating manual bottlenecks and scattered processes, MediFlow creates a connected, streamlined, and hassle-free healthcare experience for all.
                    </p>
                </div>
            </div>
        </div>
        <div class="container mb-5">
            <h2 class="text-center mb-4 text-primary fw-semibold">Why Choose MediFlow?</h2>
            <div class="row g-4 justify-content-center">
                <div class="col-md-4" v-for="(feature, i) in features" :key="i">
                    <div class="card p-4 text-center h-100 shadow-sm">
                        <i :class="feature.icon" class="feature-icon mb-3"></i>
                        <h5 class="fw-semibold">{{ feature.title }}</h5>
                        <p class="text-muted">{{ feature.desc }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "HomePage",
        data() {
            return {
                features: [{
                    icon: "bi bi-lightning-charge-fill",
                    title: "Faster Hospital Processes",
                    desc: "A modern digital workflow that cuts down waiting times, reduces repetitive manual tasks, and enables smoother, faster, and more efficient hospital operations from start to finish.",
                },{
                    icon: "bi bi-file-earmark-medical",
                    title: "Organized Medical Information",
                    desc: "Appointments, reports, and visit history remain neatly structured and instantly accessible, offering greater clarity, reducing confusion, and supporting informed medical decisions.",
                },{
                    icon: "bi bi-shield-check",
                    title: "Structured and Reliable Record Keeping",
                    desc: "Data is maintained in a consistent and well-organized digital format, ensuring accuracy, security, traceability, and dependable access whenever required.",
                }],
            };
        },
    };
</script>

<style scoped>
    .intro-text {
        padding-top: 3rem;
        padding-bottom: 2rem;
    }
    .intro-text h1 {
        font-weight: 700;
        font-size: 3rem;
    }
    .feature-icon {
        font-size: 2.4rem;
        color: #1f2f7f;
    }
</style>