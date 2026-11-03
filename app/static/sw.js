const STATIC_CACHE = 'manual-rastreabilidade-static-v1';
const CACHE_PREFIX = 'manual-rastreabilidade-static-';
const STATIC_DESTINATIONS = new Set(['style', 'script', 'image', 'font']);

self.addEventListener('install', (event) => {
    event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', (event) => {
    event.waitUntil((async () => {
        const cacheNames = await caches.keys();
        await Promise.all(
            cacheNames
                .filter((name) => name.startsWith(CACHE_PREFIX) && name !== STATIC_CACHE)
                .map((name) => caches.delete(name))
        );
        await self.clients.claim();
    })());
});

self.addEventListener('fetch', (event) => {
    const request = event.request;
    if (request.method !== 'GET' || !STATIC_DESTINATIONS.has(request.destination)) return;

    const url = new URL(request.url);
    if (url.origin === self.location.origin && (url.pathname === '/sw.js' || url.pathname === '/manifest.json')) {
        return;
    }

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
