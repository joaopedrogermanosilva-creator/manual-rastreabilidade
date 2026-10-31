(function () {
    const root = document.documentElement;
    const btn = document.getElementById('theme-toggle');
    const icon = btn.querySelector('.theme-icon');

    function aplicarTema(tema) {
        root.setAttribute('data-theme', tema);
        localStorage.setItem('theme', tema);
        icon.textContent = tema === 'dark' ? '\u25d0' : '\u25d1';
    }

    aplicarTema(root.getAttribute('data-theme') || 'dark');

    btn.addEventListener('click', () => {
        const atual = root.getAttribute('data-theme');
        aplicarTema(atual === 'dark' ? 'light' : 'dark');
    });
})();
