document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const closeMenu = document.getElementById('close-menu');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    function openMenu() {
        sidebar.classList.add('open');
        overlay.classList.add('open');
    }

    function closeMenuAction() {
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
    }

    if(menuToggle) menuToggle.addEventListener('click', openMenu);
    if(closeMenu) closeMenu.addEventListener('click', closeMenuAction);
    if(overlay) overlay.addEventListener('click', closeMenuAction);
});
