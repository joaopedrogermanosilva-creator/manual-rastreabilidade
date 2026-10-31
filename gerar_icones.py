import os

# 1. Instala a biblioteca Pillow se não estiver instalada
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Instalando Pillow para criar os ícones...")
    os.system("pip install Pillow")
    from PIL import Image, ImageDraw

# 2. Cria a pasta de imagens
os.makedirs("app/static/img", exist_ok=True)

# 3. Gera os ícones PNG (quadrado laranja com um "R" escuro)
def gerar_icone(tamanho, nome_arquivo):
    img = Image.new('RGB', (tamanho, tamanho), color='#f97316') # Laranja
    draw = ImageDraw.Draw(img)
    
    # Desenha um "R" simples e grosso (usando retângulos) para não depender de fontes do sistema
    # Linha vertical
    draw.rectangle([tamanho*0.3, tamanho*0.2, tamanho*0.4, tamanho*0.8], fill='#111')
    # Curva do R
    draw.rectangle([tamanho*0.4, tamanho*0.2, tamanho*0.7, tamanho*0.3], fill='#111')
    draw.rectangle([tamanho*0.6, tamanho*0.3, tamanho*0.7, tamanho*0.5], fill='#111')
    draw.rectangle([tamanho*0.4, tamanho*0.45, tamanho*0.7, tamanho*0.55], fill='#111')
    # Perna do R
    draw.polygon([(tamanho*0.45, tamanho*0.55), (tamanho*0.6, tamanho*0.55), (tamanho*0.7, tamanho*0.8), (tamanho*0.55, tamanho*0.8)], fill='#111')
    
    img.save(nome_arquivo)
    print(f"[ok] {nome_arquivo} criado")

gerar_icone(192, "app/static/img/icon-192.png")
gerar_icone(512, "app/static/img/icon-512.png")

# 4. Atualiza o manifest.json
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
      "purpose": "any maskable"
    },
    {
      "src": "/static/img/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
"""
with open("app/static/manifest.json", "w", encoding="utf-8") as f:
    f.write(manifest)
print("[ok] manifest.json atualizado com os ícones PNG")

# 5. Atualiza o base.html para avisar o Android e o iOS
with open("app/templates/base.html", "r", encoding="utf-8") as f:
    html = f.read()

if 'apple-touch-icon' not in html:
    tags = """
    <meta name="theme-color" content="#f97316">
    <link rel="apple-touch-icon" href="/static/img/icon-192.png">
"""
    html = html.replace('<link rel="manifest" href="/static/manifest.json">', '<link rel="manifest" href="/static/manifest.json">' + tags)
    with open("app/templates/base.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[ok] base.html atualizado com meta tags do celular")

print("\nAgora envie para o GitHub (git add, commit, push).")
