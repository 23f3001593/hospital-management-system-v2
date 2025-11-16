<template>
    <div class="container my-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="mb-0 fw-bold">{{ title }}</h2>
            <button class="btn btn-primary" @click="openUpdateAvailabilityModal">Update Availability</button>
        </div>
        <div class="card">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-striped mb-0 text-center align-middle">
                        <thead>
                            <tr>
                                <th scope="col">Day</th>
                                <th scope="col">Date</th>
                                <th scope="col">Availability</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(day, index) in orderedDays" :key="day">
                                <td>{{ day }}</td>
                                <td>{{ getDateForDay(index) }}</td>
                                <td>
                                    <div class="d-flex justify-content-center gap-2">
                                        <button
                                        class="btn fw-semibold"
                                        :class="(availability[day] && availability[day][0]) ? 'btn-success' : 'btn-danger'"
                                        style="pointer-events:none; opacity:1;"
                                        >
                                            10:00am - 01:00pm
                                        </button>
                                        <button
                                        class="btn fw-semibold"
                                        :class="(availability[day] && availability[day][1]) ? 'btn-success' : 'btn-danger'"
                                        style="pointer-events:none; opacity:1;"
                                        >
                                            04:00pm - 07:00pm
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div v-if="showUpdateAvailabilityModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content rounded-4 shadow-lg">
                    <div class="modal-header bg-primary d-flex justify-content-center align-items-center">
                        <h2 class="text-center mb-0 fw-bold">Update Availability</h2>
                    </div>
                    <div class="modal-body">
                        <div class="card">
                            <div class="card-body p-0">
                                <div class="table-responsive">
                                    <table class="table table-striped mb-0 text-center align-middle">
                                        <thead>
                                            <tr>
                                                <th scope="col">Day</th>
                                                <th scope="col">Date</th>
                                                <th scope="col">Availability</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(day, index) in orderedDays" :key="day">
                                                <td>{{ day }}</td>
                                                <td>{{ getDateForDay(index) }}</td>
                                                <td>
                                                    <div class="d-flex justify-content-center gap-2">
                                                        <button
                                                            class="btn fw-semibold"
                                                            :class="(editableAvailability[day] && editableAvailability[day][0]) ? 'btn-success' : 'btn-danger'"
                                                            @click="toggleSlot(day, 0)"
                                                        >
                                                            10:00am - 01:00pm
                                                        </button>
                                                        <button
                                                            class="btn fw-semibold"
                                                            :class="(editableAvailability[day] && editableAvailability[day][1]) ? 'btn-success' : 'btn-danger'"
                                                            @click="toggleSlot(day, 1)"
                                                        >
                                                            04:00pm - 07:00pm
                                                        </button>
                                                    </div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <div class="w-100">
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-outline-secondary w-50 me-2" @click="closeUpdateAvailabilityModal">Cancel</button>
                                <button type="button" class="btn btn-primary w-50" :disabled="loading" @click="updateAvailability">
                                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                                    <span v-else>Update</span>
                                </button>
                            </div>
                            <div v-if="errorMessage" class="text-danger text-center mt-2">{{ errorMessage }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios";
    import { handleScrollLock } from "@/utils/scroll-lock";
    import { showToast } from "@/utils/toast.js";
    export default {
        name: "AvailabilityTable",
        emits: ['availabilityChanged'],
        props: {
            title: String,
            availability: Object,
        },
        data() {
            return {
                editableAvailability: {},
                orderedDays: ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
                showUpdateAvailabilityModal: false,
                errorMessage: "",
                loading: false,
            };
        },
        watch: {
            showUpdateAvailabilityModal: 'updateScrollLock',
        },
        methods: {
            async updateAvailability() {
                this.loading = true;
                this.errorMessage = "";
                try {
                    const id = this.$store.state.user.id;
                    const response = await axios.put(`/doctor/availability/${id}`, this.editableAvailability);
                    this.closeUpdateAvailabilityModal();
                    showToast(response.data.message,'success');
                    this.$emit('availabilityChanged');
                } catch (error) {
                    if (error.response) {
                        this.errorMessage = error.response.data.message;
                    } else {
                        this.errorMessage = "Something went wrong. Please try again later.";
                    }
                } finally {
                    this.loading = false;
                }
            },
            toggleSlot(day, index) {
                if (!this.editableAvailability[day]) {
                    this.editableAvailability[day] = [false, false];
                }
                this.editableAvailability[day][index] = !this.editableAvailability[day][index];
            },
            getDateForDay(dayIndex) {
                const today = new Date();
                const todayNum = today.getDay();
                let offsetToNextMonday = (1 - todayNum + 7) % 7;
                if (offsetToNextMonday === 0) offsetToNextMonday = 7;
                const nextMonday = new Date(today);
                nextMonday.setDate(today.getDate() + offsetToNextMonday);
                const target = new Date(nextMonday);
                target.setDate(nextMonday.getDate() + dayIndex);
                return target.toLocaleDateString("en-GB", {day: "2-digit", month: "short", year: "numeric",});
            },
            updateScrollLock() {
                handleScrollLock([this.showUpdateAvailabilityModal]);
            },
            openUpdateAvailabilityModal() {
                const copy = JSON.parse(JSON.stringify(this.availability || {}));
                this.orderedDays.forEach(day => {if (!copy[day]) copy[day] = [false, false];});
                this.editableAvailability = copy;
                this.showUpdateAvailabilityModal = true;
            },
            closeUpdateAvailabilityModal() {
                this.showUpdateAvailabilityModal = false;
                this.errorMessage = "";
                this.$nextTick(() => {
                    handleScrollLock([this.showUpdateAvailabilityModal]);
                });
            },
        },
    };
</script>