export function showToast(message, type) {
    const toastEl = document.getElementById("toast");
    const bodyEl = document.getElementById("toastBody");
    toastEl.classList.remove("bg-primary", "bg-success", "bg-danger");
    toastEl.classList.add(`bg-${type}`);
    bodyEl.textContent = message;
    const toast = window.bootstrap.Toast.getOrCreateInstance(toastEl, { delay: 5000 });
    toast.show();
}