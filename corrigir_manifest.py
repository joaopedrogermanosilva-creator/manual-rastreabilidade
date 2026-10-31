import json

manifest = {
    "name": "Manual de Rastreabilidade",
    "short_name": "Rastreabilidade",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0d0d0f",
    "theme_color": "#f97316",
    "icons": [
        {
            "src": "/static/img/icon-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any"
        },
        {
            "src": "/static/img/icon-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "maskable"
        },
        {
            "src": "/static/img/icon-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any"
        },
        {
            "src": "/static/img/icon-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "maskable"
        }
    ]
}

with open("app/static/manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print("[ok] manifest.json corrigido com os campos purpose separados.")
print("Agora rode: git add . ; git commit -m 'fix manifest purpose'; git push")
