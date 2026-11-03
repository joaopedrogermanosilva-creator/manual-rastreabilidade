(() => {
    const dialog = document.getElementById("modal-info");
    const openButton = document.querySelector(".fab-btn");
    if (!(dialog instanceof HTMLDialogElement) || !(openButton instanceof HTMLButtonElement)) return;

    openButton.addEventListener("click", () => dialog.showModal());
    dialog.querySelectorAll("[data-info-close]").forEach((button) => {
        button.addEventListener("click", () => dialog.close());
    });
    dialog.addEventListener("click", (event) => {
        if (event.target === dialog) dialog.close();
    });
})();
