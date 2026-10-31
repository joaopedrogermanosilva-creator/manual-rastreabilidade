import os

# ============ 1. CRIA O MANIFEST (PARA O CELULAR) ============
manifest = """{
  "name": "Manual de Rastreabilidade",
  "short_name": "Rastreabilidade",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0d0d0f",
  "theme_color": "#f97316",
  "icons": [
    {
      "src": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI0MCIgZmlsbD0iI2Y5NzMxNiIvPjwvc3ZnPg==",
      "sizes": "192x192",
      "type": "image/svg+xml"
    }
  ]
}
"""
with open("app/static/manifest.json", "w", encoding="utf-8") as f:
    f.write(manifest)
print("[ok] manifest.json criado")

# ============ 2. CRIA O SCRIPT DO MENU ============
menu_js = """document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const closeMenu = document.getElementById('close-menu');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    function openMenu() {
        sidebar.classList.add('open');
        overlay.classList.add('open');
    }

    function closeMenuAction() {
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
    }

    if(menuToggle) menuToggle.addEventListener('click', openMenu);
    if(closeMenu) closeMenu.addEventListener('click', closeMenuAction);
    if(overlay) overlay.addEventListener('click', closeMenuAction);
});
"""
with open("app/static/js/menu.js", "w", encoding="utf-8") as f:
    f.write(menu_js)
print("[ok] menu.js criado")

# ============ 3. ATUALIZA O BASE.HTML (menu + manifest) ============
base_html = """<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Manual de Rastreabilidade{% endblock %}</title>
    <link rel="manifest" href="/static/manifest.json">
    <link rel="stylesheet" href="/static/css/style.css">
    <script>
        (function () {
            const t = localStorage.getItem('theme') || 'dark';
            document.documentElement.setAttribute('data-theme', t);
        })();
    </script>
</head>
<body>
    <div id="overlay" class="overlay"></div>
    <aside id="sidebar" class="sidebar">
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
    </aside>

    <header class="topbar">
        <div class="brand">
            <button id="menu-toggle" class="menu-btn">&#9776;</button>
            <span class="brand-mark">&#9684;&#9682;</span>
            <span class="brand-name">RASTREABILIDADE</span>
        </div>
        <button id="theme-toggle" class="theme-btn" title="Alternar tema">
            <span class="theme-icon">&#9680;</span>
        </button>
    </header>

    <main class="container">
        {% block content %}{% endblock %}
    </main>

    <script src="/static/js/theme.js"></script>
    <script src="/static/js/menu.js"></script>
</body>
</html>
"""
with open("app/templates/base.html", "w", encoding="utf-8") as f:
    f.write(base_html)
print("[ok] base.html atualizado (menu lateral)")

# ============ 4. ATUALIZA O CSS (design + menu + mobile) ============
css_extra = """

/* ===== MENU LATERAL ===== */
.overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.6);
    z-index: 998;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s;
}
.overlay.open {
    opacity: 1;
    pointer-events: all;
}

.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 280px;
    height: 100vh;
    background: var(--bg-elev);
    border-right: 1px solid var(--border);
    z-index: 999;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;
}
.sidebar.open { transform: translateX(0); }

.sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid var(--border);
}
.sidebar-header h2 { margin: 0; font-size: 18px; }
.close-btn {
    background: none;
    border: none;
    color: var(--text);
    font-size: 28px;
    cursor: pointer;
    line-height: 1;
}

.sidebar-list {
    list-style: none;
    padding: 10px 0;
    margin: 0;
    overflow-y: auto;
}
.sidebar-list li a {
    display: block;
    padding: 14px 20px;
    color: var(--text);
    text-decoration: none;
    font-size: 15px;
    transition: background 0.2s, color 0.2s;
    border-left: 3px solid transparent;
}
.sidebar-list li a:hover {
    background: var(--accent-soft);
    color: var(--accent);
    border-left-color: var(--accent);
}

.menu-btn {
    background: none;
    border: none;
    color: var(--text);
    font-size: 22px;
    cursor: pointer;
    margin-right: 10px;
    padding: 0;
}

/* ===== MOBILE ===== */
@media (max-width: 600px) {
    .container { padding: 20px 16px; }
    .hero h1 { font-size: 32px; }
    .topbar { padding: 12px 16px; }
    .acoes-tarefa { flex-direction: column; }
    .btn-editar, .btn-excluir { width: 100%; justify-content: center; }
    .grid { grid-template-columns: 1fr; }
}

/* ===== DESIGN MELHORADO ===== */
.card {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.card:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
}
.bloco {
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
"""
with open("app/static/css/style.css", "a", encoding="utf-8") as f:
    f.write(css_extra)
print("[ok] CSS atualizado (menu + mobile + design)")

# ============ 5. ATUALIZA ROUTES.PY (para o menu ter as categorias) ============
routes = """from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from supabase_client import supabase

from app.dados import (
    buscar_procedimento, adicionar_procedimento, atualizar_procedimento,
    excluir_procedimento, get_categorias, get_procedimentos_por_categoria,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html",
        context={"categorias": get_categorias()},
    )


@router.get("/categoria/{slug}", response_class=HTMLResponse)
def categoria(slug: str, request: Request):
    cats = get_categorias()
    cat = cats.get(slug)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria nao encontrada")
    return templates.TemplateResponse(
        request=request, name="categoria.html",
        context={"categoria": cat, "categoria_slug": slug, "procedimentos": get_procedimentos_por_categoria(slug), "categorias": cats},
    )


@router.get("/tarefa/novo", response_class=HTMLResponse)
def form_novo(request: Request):
    return templates.TemplateResponse(
        request=request, name="form.html",
        context={"categorias": get_categorias()},
    )


@router.post("/tarefa/novo")
def salvar_novo(
    titulo: Annotated[str, Form()], categoria: Annotated[str, Form()],
    resumo: Annotated[str, Form()], objetivo: Annotated[str, Form()],
    como_realizar: Annotated[str, Form()], pontos_atencao: Annotated[str, Form()] = "",
    arquivo: UploadFile = File(None),
):
    lista_passos = [p.strip() for p in como_realizar.strip().split("\\n") if p.strip()]
    lista_pontos = [p.strip() for p in pontos_atencao.strip().split("\\n") if p.strip()]
    arquivo_url = None
    if arquivo and arquivo.filename:
        try:
            path = f"procedimentos/{titulo.replace(' ', '_')}_{arquivo.filename}"
            supabase.storage.from_("documentos").upload(path, arquivo.file.read())
            arquivo_url = supabase.storage.from_("documentos").get_public_url(path)
        except Exception as e: print(f"Erro upload: {e}")

    adicionar_procedimento({
        "categoria": categoria, "titulo": titulo, "resumo": resumo,
        "objetivo": objetivo, "como_realizar": lista_passos,
        "pontos_atencao": lista_pontos, "arquivo_url": arquivo_url,
    })
    return RedirectResponse(url=f"/categoria/{categoria}", status_code=303)


@router.get("/tarefa/{proc_id}/editar", response_class=HTMLResponse)
def form_editar(proc_id: int, request: Request):
    proc = buscar_procedimento(proc_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Procedimento nao encontrado")
    return templates.TemplateResponse(
        request=request, name="form_editar.html",
        context={"proc": proc, "categorias": get_categorias()},
    )


@router.post("/tarefa/{proc_id}/editar")
def salvar_edicao(
    proc_id: int, titulo: Annotated[str, Form()], categoria: Annotated[str, Form()],
    resumo: Annotated[str, Form()], objetivo: Annotated[str, Form()],
    como_realizar: Annotated[str, Form()], pontos_atencao: Annotated[str, Form()] = "",
    arquivo: UploadFile = File(None),
):
    lista_passos = [p.strip() for p in como_realizar.strip().split("\\n") if p.strip()]
    lista_pontos = [p.strip() for p in pontos_atencao.strip().split("\\n") if p.strip()]
    proc_atual = buscar_procedimento(proc_id)
    arquivo_url = proc_atual.get("arquivo_url") if proc_atual else None

    if arquivo and arquivo.filename:
        try:
            path = f"procedimentos/{titulo.replace(' ', '_')}_{arquivo.filename}"
            supabase.storage.from_("documentos").upload(path, arquivo.file.read(), {"upsert": "true"})
            arquivo_url = supabase.storage.from_("documentos").get_public_url(path)
        except Exception as e: print(f"Erro upload: {e}")

    atualizar_procedimento(proc_id, {
        "categoria": categoria, "titulo": titulo, "resumo": resumo,
        "objetivo": objetivo, "como_realizar": lista_passos,
        "pontos_atencao": lista_pontos, "arquivo_url": arquivo_url,
    })
    return RedirectResponse(url=f"/tarefa/{proc_id}", status_code=303)


@router.post("/tarefa/{proc_id}/excluir")
def excluir(proc_id: int):
    proc = buscar_procedimento(proc_id)
    if not proc: raise HTTPException(status_code=404, detail="Procedimento nao encontrado")
    cat_slug = proc["categoria_slug"]
    excluir_procedimento(proc_id)
    return RedirectResponse(url=f"/categoria/{cat_slug}", status_code=303)


@router.get("/tarefa/{proc_id}", response_class=HTMLResponse)
def tarefa(proc_id: int, request: Request):
    proc = buscar_procedimento(proc_id)
    if not proc: raise HTTPException(status_code=404, detail="Procedimento nao encontrado")
    cats = get_categorias()
    cat = cats.get(proc["categoria_slug"], {"titulo": proc["categoria_slug"]})
    return templates.TemplateResponse(
        request=request, name="tarefa.html",
        context={"proc": proc, "categoria": cat, "categorias": cats},
    )
"""
with open("app/routes.py", "w", encoding="utf-8") as f:
    f.write(routes)
print("[ok] routes.py atualizado (menu em todas as paginas)")

print("\nTudo pronto! O uvicorn vai reiniciar sozinho. Dê Ctrl+F5 no navegador.")
