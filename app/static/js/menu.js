document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const closeMenu = document.getElementById('close-menu');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const folderFilter = document.getElementById('sidebar-folder-filter');
    const folderList = document.getElementById('sidebar-folders');
    const folderEmpty = document.getElementById('sidebar-folder-empty');
    const progressBar = document.getElementById('progress-bar');
    let progressTimer;
    let progressResetTimer;

    function startProgress() {
        if (!(progressBar instanceof HTMLElement)) return;
        window.clearTimeout(progressTimer);
        window.clearTimeout(progressResetTimer);
        progressBar.classList.remove('is-complete');
        progressBar.classList.add('is-active');
        progressBar.style.width = '50%';
        progressTimer = window.setTimeout(() => {
            progressBar.style.width = '80%';
        }, 180);
    }

    function completeProgress() {
        if (!(progressBar instanceof HTMLElement)) return;
        window.clearTimeout(progressTimer);
        progressBar.classList.add('is-active');
        progressBar.style.width = '100%';
        progressBar.classList.add('is-complete');
        progressResetTimer = window.setTimeout(() => {
            progressBar.style.width = '0%';
            progressBar.classList.remove('is-active', 'is-complete');
        }, 350);
    }

    function isNavigationClick(event, link) {
        if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
            return false;
        }
        if (link.hasAttribute('download') || (link.target && link.target !== '_self')) return false;

        const href = link.getAttribute('href');
        if (!href || href.startsWith('#')) return false;
        const destination = new URL(href, window.location.href);
        return destination.origin === window.location.origin
            && (destination.pathname !== window.location.pathname
                || destination.search !== window.location.search
                || destination.hash !== window.location.hash);
    }

    document.addEventListener('click', (event) => {
        if (!(event.target instanceof Element)) return;
        const link = event.target.closest('a[href]');
        if (link instanceof HTMLAnchorElement && isNavigationClick(event, link)) {
            startProgress();
        }
    }, true);

    document.addEventListener('submit', (event) => {
        if (!(event.target instanceof HTMLFormElement)) return;
        if (
            event.target.matches('[data-confirmation]')
            && event.target.dataset.confirmed !== 'true'
        ) {
            return;
        }
        startProgress();

        if (!event.target.matches('[data-loading-form]')) return;
        const submitButton = event.submitter instanceof HTMLButtonElement
            ? event.submitter
            : event.target.querySelector('button[type="submit"]:not([form])');
        if (!(submitButton instanceof HTMLButtonElement)) return;

        submitButton.disabled = true;
        submitButton.classList.add('is-processing');
        const label = submitButton.querySelector('[data-submit-label]');
        if (label) {
            label.textContent = '⏳ Processando...';
        } else {
            submitButton.textContent = '⏳ Processando...';
        }
    });

    window.addEventListener('pageshow', completeProgress);

    function filterFolder(item, query) {
        const folderLink = item.querySelector(':scope > .sidebar-folder-link');
        const matchesFolder = folderLink instanceof HTMLAnchorElement
            && folderLink.textContent.toLocaleLowerCase().includes(query);
        const childItems = item.querySelectorAll(':scope > .sidebar-sublist > .sidebar-folder-item');
        let matchesChild = false;

        childItems.forEach((child) => {
            if (filterFolder(child, query)) matchesChild = true;
        });

        const isVisible = !query || matchesFolder || matchesChild;
        item.hidden = !isVisible;
        return isVisible;
    }

    function filterFolders() {
        if (!(folderFilter instanceof HTMLInputElement) || !(folderList instanceof HTMLUListElement)) return;
        const query = folderFilter.value.trim().toLocaleLowerCase();
        const rootFolders = folderList.querySelectorAll(':scope > .sidebar-folder-item');
        let visibleCount = 0;
        rootFolders.forEach((folder) => {
            if (filterFolder(folder, query)) visibleCount += 1;
        });
        if (folderEmpty instanceof HTMLElement) {
            folderEmpty.hidden = !query || visibleCount > 0;
        }
    }

    if (folderFilter instanceof HTMLInputElement) {
        folderFilter.addEventListener('input', filterFolders);
    }

    function openMenu() {
        if (!sidebar || !overlay) return;
        sidebar.classList.add('open');
        overlay.classList.add('open');
    }

    function closeMenuAction() {
        if (!sidebar || !overlay) return;
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
    }

    if (menuToggle) menuToggle.addEventListener('click', openMenu);
    if (closeMenu) closeMenu.addEventListener('click', closeMenuAction);
    if (overlay) overlay.addEventListener('click', closeMenuAction);
    if (sidebar) {
        sidebar.addEventListener('click', (event) => {
            if (event.target instanceof Element && event.target.closest('a')) {
                closeMenuAction();
            }
        }, true);
    }
});
