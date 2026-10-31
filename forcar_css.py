# Lê o base.html atual
with open("app/templates/base.html", "r", encoding="utf-8") as f:
    html = f.read()

# Força o navegador a baixar o CSS novo adicionando ?v=2 no link
html = html.replace(
    '<link rel="stylesheet" href="/static/css/style.css">',
    '<link rel="stylesheet" href="/static/css/style.css?v=2">'
)

with open("app/templates/base.html", "w", encoding="utf-8") as f:
    f.write(html)
print("[ok] base.html atualizado com cache-buster no CSS")
