(() => {
    const dialog = document.getElementById("modal-confirmacao");
    if (!dialog) return;

    const message = document.getElementById("modal-confirmacao-mensagem");
    const cancelButton = dialog.querySelector("[data-confirm-cancel]");
    const submitButton = dialog.querySelector("[data-confirm-submit]");
    let pendingForm = null;
    let pendingSubmitter = null;

    document.addEventListener("submit", (event) => {
        const form = event.target;
        if (!(form instanceof HTMLFormElement) || !form.hasAttribute("data-confirmation")) return;
        if (form.dataset.confirmed === "true") {
            delete form.dataset.confirmed;
            return;
        }

        event.preventDefault();
        pendingForm = form;
        pendingSubmitter = event.submitter instanceof HTMLElement ? event.submitter : null;
        message.textContent = form.dataset.confirmMessage || "Tem certeza de que deseja excluir este item?";
        dialog.showModal();
    });

    cancelButton.addEventListener("click", () => dialog.close("cancel"));
    submitButton.addEventListener("click", () => {
        if (!pendingForm) return;
        const form = pendingForm;
        const submitter = pendingSubmitter;
        pendingForm = null;
        pendingSubmitter = null;
        form.dataset.confirmed = "true";
        dialog.close("confirm");
        if (submitter && submitter.form === form) {
            form.requestSubmit(submitter);
        } else {
            form.requestSubmit();
        }
    });

    dialog.addEventListener("click", (event) => {
        if (event.target === dialog) dialog.close("cancel");
    });
    dialog.addEventListener("close", () => {
        pendingForm = null;
        pendingSubmitter = null;
    });
})();
