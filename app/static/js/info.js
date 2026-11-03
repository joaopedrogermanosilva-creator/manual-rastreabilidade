(() => {
    const dialog = document.getElementById("modal-info");
    const openButton = document.querySelector(".fab-btn");
    const hideCheckbox = document.getElementById("esconder-ajuda");
    const restoreButton = document.querySelector("[data-info-restore]");
    const storageKey = "ocultar_fab";
    const isHome = window.location.pathname === "/";

    function updateVisibility() {
        const hiddenOnInternalPages = localStorage.getItem(storageKey) === "true" && !isHome;
        if (openButton instanceof HTMLButtonElement) {
            openButton.hidden = hiddenOnInternalPages;
        }
        if (restoreButton instanceof HTMLButtonElement) {
            restoreButton.hidden = localStorage.getItem(storageKey) !== "true";
        }
    }

    function savePreference() {
        if (!(hideCheckbox instanceof HTMLInputElement)) return;
        if (hideCheckbox.checked) {
            localStorage.setItem(storageKey, "true");
        } else {
            localStorage.removeItem(storageKey);
        }
        updateVisibility();
    }

    if (dialog instanceof HTMLDialogElement && openButton instanceof HTMLButtonElement) {
        openButton.addEventListener("click", () => {
            if (hideCheckbox instanceof HTMLInputElement) {
                hideCheckbox.checked = localStorage.getItem(storageKey) === "true";
            }
            dialog.showModal();
        });
        dialog.querySelectorAll("[data-info-close]").forEach((button) => {
            button.addEventListener("click", () => dialog.close());
        });
        dialog.addEventListener("click", (event) => {
            if (event.target === dialog) dialog.close();
        });
        dialog.addEventListener("close", savePreference);
    }

    if (hideCheckbox instanceof HTMLInputElement) {
        hideCheckbox.addEventListener("change", savePreference);
    }
    if (restoreButton instanceof HTMLButtonElement) {
        restoreButton.addEventListener("click", () => {
            localStorage.removeItem(storageKey);
            if (hideCheckbox instanceof HTMLInputElement) {
                hideCheckbox.checked = false;
            }
            updateVisibility();
        });
    }

    updateVisibility();
})();
