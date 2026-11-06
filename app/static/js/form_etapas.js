document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("etapas-container");
    const addButton = document.getElementById("adicionar-etapa");
    if (!(container instanceof HTMLElement) || !(addButton instanceof HTMLButtonElement)) return;

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
        if (!(fileInput instanceof HTMLInputElement) || !(orderInput instanceof HTMLInputElement)) return;

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
            } else {
                fileInput.removeAttribute("name");
                orderInput.removeAttribute("name");
            }
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
            <label>Foto da etapa <small>(opcional)</small></label>
            <input type="hidden" data-photo-order>
            <input type="file" data-field="passos_fotos" accept="image/jpeg,image/png,image/gif,image/webp,.jpg,.jpeg,.png,.gif,.webp">
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
    container.addEventListener("click", (event) => {
        if (!(event.target instanceof Element)) return;
        const removeButton = event.target.closest(".btn-remover-etapa");
        if (!removeButton) return;
        removeButton.closest(".etapa-form-card")?.remove();
        atualizarNumeracao();
    });

    if (!container.querySelector(".etapa-form-card")) adicionarEtapa();
    container.querySelectorAll(".etapa-form-card").forEach(configurarUploadFoto);
    atualizarNumeracao();
});
