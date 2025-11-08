<template>
    <div class="toast-container position-fixed bottom-0 start-50 translate-middle-x p-3">
        <div id="toast" class="toast align-items-center border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body" id="toastBody"></div>
                <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Toast",
    }
</script>

<style scoped>    
    .toast {
        width: auto;
        max-width: 100%;
    }
    .toast .btn-close {
        filter: invert(1) brightness(200%);
        opacity: 1;
    }
    .toast .btn-close:focus, .toast .btn-close:active {
        box-shadow: none !important;
    }
</style>