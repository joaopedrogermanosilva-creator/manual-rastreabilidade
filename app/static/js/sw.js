// Service Worker básico para permitir a instalação como PWA
self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', (e) => {
  // Deixa o navegador lidar com as requisições normalmente
});
