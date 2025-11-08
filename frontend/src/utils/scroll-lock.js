export function handleScrollLock(modalStates) {
    const anyModalOpen = modalStates.some(state => state);
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    if (anyModalOpen) {
        document.body.style.overflow = "hidden";
        document.body.style.paddingRight = `${scrollbarWidth}px`;
    } else {
        document.body.style.overflow = "";
        document.body.style.paddingRight = "";
    }
}