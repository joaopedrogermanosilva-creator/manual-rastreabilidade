document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("etapas-container");
    const addButton = document.getElementById("adicionar-etapa");
    if (!(container instanceof HTMLElement) || !(addButton instanceof HTMLButtonElement)) return;
    const confirmationDialog = document.getElementById("modal-confirmacao");
    const confirmationMessage = document.getElementById("modal-confirmacao-mensagem");
    const confirmRemovalButton = confirmationDialog?.querySelector("[data-confirm-submit]");
    let pendingStageRemoval = null;

    function atualizarNumeracao() {
        container.querySelectorAll(".etapa-form-card").forEach((card, index) => {
            const titulo = card.querySelector(".etapa-card-header strong");
            if (titulo) titulo.textContent = `Etapa ${index + 1}`;
            const fileInput = card.querySelector('input[data-field="passos_fotos"]');
            const orderInput = card.querySelector("[data-photo-order]");
            if (fileInput?.name === "passos_fotos" && orderInput) {
                orderInput.value = String(index);
            }
        });
    }

    function configurarUploadFoto(card) {
        const fileInput = card.querySelector('input[data-field="passos_fotos"]');
        const orderInput = card.querySelector("[data-photo-order]");
        const existingPhotoInput = card.querySelector('input[name="passos_fotos_existentes"]');
        const removePhotoFlag = card.querySelector('input[name="remover_fotos"]');
        const removePhotoButton = card.querySelector(".btn-remover-foto");
        const preview = card.querySelector(".etapa-foto-existente, .etapa-foto-atual");
        if (
            !(fileInput instanceof HTMLInputElement)
            || !(orderInput instanceof HTMLInputElement)
            || !(existingPhotoInput instanceof HTMLInputElement)
            || !(removePhotoFlag instanceof HTMLInputElement)
            || !(removePhotoButton instanceof HTMLButtonElement)
        ) return;

        fileInput.addEventListener("change", () => {
            const file = fileInput.files?.[0];
            if (file && file.size > 20 * 1024 * 1024) {
                alert(`A foto ${file.name} excede o limite de 20 MB.`);
                fileInput.value = "";
            }
            if (fileInput.files?.length) {
                fileInput.name = "passos_fotos";
                orderInput.name = "passos_fotos_ordem";
                orderInput.value = String([...container.querySelectorAll(".etapa-form-card")].indexOf(card));
                removePhotoButton.hidden = false;
            } else {
                fileInput.removeAttribute("name");
                orderInput.removeAttribute("name");
                removePhotoButton.hidden = !existingPhotoInput.value;
            }
        });

        removePhotoButton.addEventListener("click", () => {
            fileInput.value = "";
            fileInput.removeAttribute("name");
            orderInput.removeAttribute("name");
            existingPhotoInput.value = "";
            removePhotoFlag.value = "1";
            removePhotoButton.hidden = true;
            if (preview) preview.hidden = true;
        });
    }

    function adicionarEtapa(texto = "", fotoUrl = "") {
        const card = document.createElement("article");
        card.className = "etapa-card etapa-form-card";
        card.innerHTML = `
            <header class="etapa-card-header">
                <strong></strong>
                <button type="button" class="btn-remover-etapa" aria-label="Remover etapa">
                    <i class="ph ph-trash"></i> Remover
                </button>
            </header>
            <label>Instrução</label>
            <textarea name="passos_texto" rows="4" placeholder="Descreva esta etapa"></textarea>
            <input type="hidden" name="passos_fotos_existentes" value="">
            <div class="etapa-foto-atual" hidden></div>
            <input type="hidden" name="remover_fotos" value="">
            <label>Foto da etapa <small>(opcional)</small></label>
            <input type="hidden" data-photo-order>
            <input type="file" data-field="passos_fotos" accept="image/jpeg,image/png,image/gif,image/webp,.jpg,.jpeg,.png,.gif,.webp">
            <button type="button" class="btn-remover-foto" hidden>🗑️ Remover Foto</button>
        `;
        card.querySelector('textarea[name="passos_texto"]').value = texto;
        if (fotoUrl) {
            const hiddenInput = card.querySelector('input[name="passos_fotos_existentes"]');
            const preview = card.querySelector(".etapa-foto-atual");
            const link = document.createElement("a");
            const image = document.createElement("img");
            link.href = fotoUrl;
            link.target = "_blank";
            link.rel = "noopener noreferrer";
            image.src = fotoUrl;
            image.alt = "Foto atual da etapa";
            image.loading = "lazy";
            link.append(image);
            preview.append(link, document.createTextNode("Foto atual — selecione outra para substituir"));
            preview.hidden = false;
            hiddenInput.value = fotoUrl;
        }
        configurarUploadFoto(card);
        container.append(card);
        atualizarNumeracao();
        return card;
    }

    addButton.addEventListener("click", () => adicionarEtapa());
    if (
        confirmationDialog instanceof HTMLDialogElement
        && confirmationMessage instanceof HTMLElement
        && confirmRemovalButton instanceof HTMLButtonElement
    ) {
        container.addEventListener("click", (event) => {
            if (!(event.target instanceof Element)) return;
            const removeButton = event.target.closest(".btn-remover-etapa");
            if (!removeButton) return;
            const card = removeButton.closest(".etapa-form-card");
            if (!card) return;
            event.preventDefault();
            pendingStageRemoval = card;
            confirmationMessage.textContent = "Deseja realmente excluir esta etapa?";
            confirmationDialog.showModal();
        });
        confirmRemovalButton.addEventListener("click", () => {
            if (!pendingStageRemoval) return;
            pendingStageRemoval.remove();
            pendingStageRemoval = null;
            atualizarNumeracao();
            confirmationDialog.close("confirm");
        });
        confirmationDialog.addEventListener("close", () => {
            pendingStageRemoval = null;
        });
    }

    container.closest("form")?.addEventListener("submit", (event) => {
        const cards = [...container.querySelectorAll(".etapa-form-card")];
        const etapaSemTexto = cards.find((card) => {
            const texto = card.querySelector('textarea[name="passos_texto"]');
            const foto = card.querySelector('input[data-field="passos_fotos"]');
            return foto.files?.length && !texto.value.trim();
        });
        if (etapaSemTexto) {
            event.preventDefault();
            alert("Descreva a etapa antes de anexar uma foto.");
            etapaSemTexto.querySelector('textarea[name="passos_texto"]').focus();
            return;
        }
        if (cards.length && !cards.some((card) => card.querySelector('textarea[name="passos_texto"]').value.trim())) {
            event.preventDefault();
            alert("Adicione o texto de pelo menos uma etapa.");
            cards[0].querySelector('textarea[name="passos_texto"]').focus();
            return;
        }
        atualizarNumeracao();
    });
    if (!container.querySelector(".etapa-form-card")) adicionarEtapa();
    container.querySelectorAll(".etapa-form-card").forEach(configurarUploadFoto);
    atualizarNumeracao();
});
