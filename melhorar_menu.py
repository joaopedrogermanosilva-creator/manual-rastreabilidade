import os

# ============ 1. ATUALIZA O BASE.HTML (Botão no rodapé + novos ícones) ============
with open("app/templates/base.html", "r", encoding="utf-8") as f:
    base = f.read()

# Substitui o bloco da sidebar
sidebar_antiga = """    <aside id="sidebar" class="sidebar">
        <div class="sidebar-header">
            <h2>Categorias</h2>
            <button id="close-menu" class="close-btn">&times;</button>
        </div>
        <ul class="sidebar-list">
            <li><a href="/">&#127968; Início</a></li>
            {% for slug, cat in categorias.items() %}
            <li><a href="/categoria/{{ slug }}">&#128193; {{ cat.titulo }}</a></li>
            {% endfor %}
        </ul>
    </aside>"""

sidebar_nova = """    <aside id="sidebar" class="sidebar">
        <div class="sidebar-header">
            <h2>Menu</h2>
            <button id="close-menu" class="close-btn">&times;</button>
        </div>
        <ul class="sidebar-list">
            <li><a href="/">&#127968; Início</a></li>
            {% for slug, cat in categorias.items() %}
            <li><a href="/categoria/{{ slug }}">&#128196; {{ cat.titulo }}</a></li>
            {% endfor %}
        </ul>
        <div class="sidebar-footer">
            <a href="/tarefa/novo" class="btn-primary" onclick="return confirm('Tem certeza que deseja adicionar um novo procedimento?');">+ Novo Procedimento</a>
        </div>
    </aside>"""

if sidebar_antiga in base:
    base = base.replace(sidebar_antiga, sidebar_nova)
    with open("app/templates/base.html", "w", encoding="utf-8") as f:
        f.write(base)
    print("[ok] base.html atualizado (Botão no menu e ícones de documento)")
else:
    # Tenta substituir o ícone de pasta de qualquer forma, caso o texto exato tenha mudado
    base = base.replace('&#128193;', '&#128196;')
    with open("app/templates/base.html", "w", encoding="utf-8") as f:
        f.write(base)
    print("[ok] base.html atualizado (ícones trocados)")

# ============ 2. ATUALIZA O CSS (Rodapé do menu) ============
with open("app/static/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

if ".sidebar-footer" not in css:
    css += """

/* ===== RODAPÉ DO MENU LATERAL ===== */
.sidebar-list {
    flex: 1;
    overflow-y: auto;
}
.sidebar-footer {
    padding: 20px;
    border-top: 1px solid var(--border);
    background: var(--bg-elev);
}
.sidebar-footer .btn-primary {
    display: block;
    text-align: center;
    width: 100%;
    text-decoration: none;
    padding: 14px;
    font-size: 15px;
    box-sizing: border-box;
}
"""
    with open("app/static/css/style.css", "w", encoding="utf-8") as f:
        f.write(css)
    print("[ok] CSS atualizado (estilo do botão no menu)")

# ============ 3. ATUALIZA O INDEX.HTML (Atalhos rápidos com novos ícones) ============
with open("app/templates/index.html", "r", encoding="utf-8") as f:
    idx = f.read()

idx = idx.replace('&#128193;', '&#128196;') # Troca pasta por documento nos atalhos rápidos

with open("app/templates/index.html", "w", encoding="utf-8") as f:
    f.write(idx)
print("[ok] index.html atualizado (ícones dos atalhos)")

print("\nTudo pronto! Dê Ctrl+Shift+R no navegador.")
