# ============ 1. CRIA O SERVICE WORKER (sw.js) ============
sw_js = """// Service Worker básico para permitir a instalação como PWA
self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', (e) => {
  // Deixa o navegador lidar com as requisições normalmente
});
"""
with open("app/static/js/sw.js", "w", encoding="utf-8") as f:
    f.write(sw_js)
print("[ok] Service Worker (sw.js) criado")

# ============ 2. REGISTRA O SERVICE WORKER NO BASE.HTML ============
with open("app/templates/base.html", "r", encoding="utf-8") as f:
    html = f.read()

if "navigator.serviceWorker" not in html:
    script_registro = """
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/static/js/sw.js')
                    .then(reg => console.log('Service Worker registrado!', reg))
                    .catch(err => console.log('Erro no Service Worker', err));
            });
        }
    </script>
"""
    html = html.replace("</body>", script_registro + "\n</body>")
    
    with open("app/templates/base.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[ok] base.html atualizado (registro do Service Worker)")
else:
    print("[ok] Service Worker já estava registrado no base.html")

print("\nAgora precisamos enviar para o GitHub.")
