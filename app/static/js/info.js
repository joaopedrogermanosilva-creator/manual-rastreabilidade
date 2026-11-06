(() => {
    const dialog = document.getElementById("modal-info");
    const openButton = document.querySelector(".fab-btn");
    const hideCheckbox = document.getElementById("esconder-ajuda");
    const restoreButton = document.querySelector("[data-info-restore]");
    const companyDialog = document.getElementById("modal-empresa");
    const companyOpenButton = document.getElementById("btn-perfil");
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

    if (companyDialog instanceof HTMLDialogElement && companyOpenButton instanceof HTMLButtonElement) {
        companyOpenButton.addEventListener("click", () => companyDialog.showModal());
        companyDialog.querySelectorAll("[data-empresa-close]").forEach((button) => {
            button.addEventListener("click", () => companyDialog.close());
        });
        companyDialog.addEventListener("click", (event) => {
            if (event.target === companyDialog) companyDialog.close();
        });
    }

    document.querySelectorAll(".ramais-search").forEach((searchInput) => {
        if (!(searchInput instanceof HTMLInputElement)) return;
        searchInput.addEventListener("input", () => {
            const query = searchInput.value.trim().toLocaleLowerCase();
            const list = searchInput.parentElement?.querySelector(".ramais-container");
            if (!list) return;

            list.querySelectorAll(".ramal-item").forEach((item) => {
                item.style.display = item.textContent.trim().toLocaleLowerCase().includes(query)
                    ? "flex"
                    : "none";
            });
        });
    });

    updateVisibility();
})();
