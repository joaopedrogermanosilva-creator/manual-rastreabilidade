const STATIC_CACHE = 'manual-rastreabilidade-static-v2';
const PAGES_CACHE = 'manual-rastreabilidade-pages-v1';
const STATIC_CACHE_PREFIX = 'manual-rastreabilidade-static-';
const PAGES_CACHE_PREFIX = 'manual-rastreabilidade-pages-';
const STATIC_DESTINATIONS = new Set(['style', 'script', 'image', 'font']);

self.addEventListener('install', (event) => {
    event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', (event) => {
    event.waitUntil((async () => {
        const cacheNames = await caches.keys();
        await Promise.all(
            cacheNames
                .filter((name) => (
                    (name.startsWith(STATIC_CACHE_PREFIX) && name !== STATIC_CACHE)
                    || (name.startsWith(PAGES_CACHE_PREFIX) && name !== PAGES_CACHE)
                ))
                .map((name) => caches.delete(name))
        );
        await self.clients.claim();
    })());
});

self.addEventListener('fetch', (event) => {
    const request = event.request;
    const url = new URL(request.url);
    if (request.method !== 'GET' || url.origin !== self.location.origin) return;

    if (request.mode === 'navigate') {
        if (url.pathname.startsWith('/admin/')) return;

        event.respondWith((async () => {
            try {
                const response = await fetch(request);
                if (response.ok && response.headers.get('content-type')?.includes('text/html')) {
                    try {
                        const cache = await caches.open(PAGES_CACHE);
                        await cache.put(request, response.clone());
                    } catch (error) {
                        console.warn('HTML page could not be cached for offline use.', error);
                    }
                }
                return response;
            } catch (networkError) {
                try {
                    const cache = await caches.open(PAGES_CACHE);
                    const cachedResponse = await cache.match(request);
                    if (cachedResponse) return cachedResponse;
                } catch (cacheError) {
                    console.warn('Cached HTML page could not be read.', cacheError);
                }
                throw networkError;
            }
        })());
        return;
    }

    if (!STATIC_DESTINATIONS.has(request.destination)) return;

    event.respondWith((async () => {
        const cache = await caches.open(STATIC_CACHE);
        const cachedResponse = await cache.match(request);
        if (cachedResponse) return cachedResponse;

        const response = await fetch(request);
        if (response.ok || response.type === 'opaque') {
            try {
                await cache.put(request, response.clone());
            } catch (error) {
                console.warn('Static asset could not be cached.', error);
            }
        }
        return response;
    })());
});
