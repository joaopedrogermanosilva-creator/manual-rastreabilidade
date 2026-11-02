(() => {
    const maxFileSize = 20 * 1024 * 1024;
    const fileInputs = document.querySelectorAll('input[type="file"][name="arquivos"]');

    fileInputs.forEach((input) => {
        input.addEventListener("change", () => {
            const oversizedFile = Array.from(input.files).find((file) => file.size > maxFileSize);
            if (!oversizedFile) return;

            alert(`O arquivo ${oversizedFile.name} é muito grande. O limite é 20MB. Vídeos maiores devem ser enviados via YouTube.`);
            input.value = "";
        });
    });
})();
