import os
from PIL import Image, ImageDraw

# ============ 1. ARRUMA O SERVICE WORKER (Vai para a raiz) ============
sw_js = """self.addEventListener('install', (e) => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(clients.claim()));
self.addEventListener('fetch', (e) => {});
"""
with open("app/static/sw.js", "w", encoding="utf-8") as f:
    f.write(sw_js)
print("[ok] sw.js movido para a pasta static raiz")

# ============ 2. GERA ÍCONES COM MARGEM (Maskable) ============
os.makedirs("app/static/img", exist_ok=True)

def gerar_icone(tamanho, nome_arquivo):
    # Fundo laranja
    img = Image.new('RGB', (tamanho, tamanho), color='#f97316')
    draw = ImageDraw.Draw(img)
    
    # Desenha o "R" um pouco menor (com margem de 20% para o Android não cortar)
    m = tamanho * 0.2 # Margem
    w = tamanho - (2 * m)
    
    # Linha vertical do R
    draw.rectangle([m + w*0.2, m + w*0.1, m + w*0.4, m + w*0.9], fill='#111')
    # Curva do R
    draw.rectangle([m + w*0.4, m + w*0.1, m + w*0.8, m + w*0.25], fill='#111')
    draw.rectangle([m + w*0.7, m + w*0.25, m + w*0.8, m + w*0.5], fill='#111')
    draw.rectangle([m + w*0.4, m + w*0.4, m + w*0.8, m + w*0.55], fill='#111')
    # Perna do R
    draw.polygon([(m + w*0.5, m + w*0.5), (m + w*0.65, m + w*0.5), (m + w*0.8, m + w*0.9), (m + w*0.6, m + w*0.9)], fill='#111')
    
    img.save(nome_arquivo)
    print(f"[ok] {nome_arquivo} recriado")

gerar_icone(192, "app/static/img/icon-192.png")
gerar_icone(512, "app/static/img/icon-512.png")

# ============ 3. ATUALIZA O MANIFEST ============
manifest = """{
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
      "src": "/static/img/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    }
  ]
}
"""
with open("app/static/manifest.json", "w", encoding="utf-8") as f:
    f.write(manifest)
print("[ok] manifest.json atualizado")

# ============ 4. ATUALIZA O BASE.HTML ============
with open("app/templates/base.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove o script antigo se existir e adiciona o novo (na raiz)
import re
html = re.sub(r"<script>\s*if\s*\('serviceWorker'\s*in\s*navigator\).*?</script>", "", html, flags=re.DOTALL)

script_novo = """
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/static/sw.js', { scope: '/' })
                    .then(reg => console.log('Service Worker OK'))
                    .catch(err => console.log('Service Worker Falhou', err));
            });
        }
    </script>
"""
html = html.replace("</body>", script_novo + "\n</body>")

with open("app/templates/base.html", "w", encoding="utf-8") as f:
    f.write(html)
print("[ok] base.html atualizado com o novo registro de SW")

print("\nAgora rode: git add . ; git commit -m 'fix pwa'; git push")
