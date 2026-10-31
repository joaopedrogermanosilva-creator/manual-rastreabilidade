import os

# ============ 1. ATUALIZA O DADOS.PY (Adiciona a função de busca) ============
with open("app/dados.py", "r", encoding="utf-8") as f:
    dados = f.read()

if "def buscar_procedimentos" not in dados:
    dados += '''

def buscar_procedimentos(termo):
    """Busca global usando ilike no Supabase."""
    if not termo:
        return []
    # O Supabase permite busca com .or_ para verificar múltiplas colunas
    response = supabase.table("procedimentos").select("*").or_(
        f"titulo.ilike.%{termo}%,resumo.ilike.%{termo}%,objetivo.ilike.%{termo}%"
    ).execute()
    return response.data
'''
    with open("app/dados.py", "w", encoding="utf-8") as f:
        f.write(dados)
    print("[ok] dados.py atualizado (busca global)")

# ============ 2. ATUALIZA O ROUTES.PY (Rota de busca) ============
with open("app/routes.py", "r", encoding="utf-8") as f:
    code = f.read()

if 'def buscar(' not in code:
    # Adiciona a rota de busca
    rota_busca = '''

@router.get("/buscar", response_class=HTMLResponse)
def buscar(request: Request, q: str = ""):
    resultados = buscar_procedimentos(q) if q else []
    return templates.TemplateResponse(
        request=request, name="busca.html",
        context={"resultados": resultados, "termo": q, "categorias": get_categorias()},
    )

'''
    # Coloca logo depois da rota home
    code = code.replace('@router.get("/categoria/{slug}"', rota_busca + '@router.get("/categoria/{slug}"')
    
    # Adiciona o import
    code = code.replace(
        "get_categorias, get_procedimentos_por_categoria,",
        "get_categorias, get_procedimentos_por_categoria, buscar_procedimentos,"
    )
    with open("app/routes.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("[ok] routes.py atualizado (rota /buscar)")

# ============ 3. NOVO INDEX.HTML (Tela de boas-vindas) ============
index_html = """{% extends "base.html" %}
{% block title %}Central de Consulta{% endblock %}
{% block content %}
<section class="landing-hero">
    <div class="landing-content">
        <h1>Central de Consulta<span class="accent">.</span></h1>
        <p class="subtitle" style="font-size: 18px;">Tudo o que você precisa para a operação de recebimento, na palma da mão.</p>
        
        <form action="/buscar" method="GET" class="search-bar-wrapper">
            <div class="search-bar">
                <span class="search-icon">&#128269;</span>
                <input type="text" name="q" placeholder="Pesquisar procedimentos, documentos, escala..." autocomplete="off">
                <button type="submit" class="btn-search">Buscar</button>
            </div>
        </form>
        
        <div class="quick-links">
            <a href="/categoria/operacoes" class="quick-link">&#128193; Operações</a>
            <a href="/categoria/documentos" class="quick-link">&#128193; Documentos</a>
            <a href="/categoria/escala" class="quick-link">&#128193; Escala</a>
            <a href="/categoria/rastreio" class="quick-link">&#128193; Rastreio</a>
        </div>
    </div>
</section>
{% endblock %}
"""
with open("app/templates/index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
print("[ok] index.html transformado na nova tela inicial")

# ============ 4. NOVO BUSCA.HTML ============
busca_html = """{% extends "base.html" %}
{% block title %}Resultados da busca{% endblock %}
{% block content %}
<section class="hero">
    <a href="/" class="back-link">&#8592; Voltar para o início</a>
    <h1>Resultados para: "{{ termo }}"<span class="accent">.</span></h1>
    <p class="subtitle">{{ resultados|length }} procedimento(s) encontrado(s).</p>
</section>

<section>
    {% if resultados %}
    <div class="grid">
        {% for p in resultados %}
        <a class="card" href="/tarefa/{{ p.id }}">
            <span class="card-tag">{{ p.categoria_slug|capitalize }}</span>
            <h3>{{ p.titulo }}</h3>
            <p>{{ p.resumo }}</p>
        </a>
        {% endfor %}
    </div>
    {% else %}
    <p class="aviso-fase">Nenhum resultado encontrado para "{{ termo }}".</p>
    {% endif %}
</section>
{% endblock %}
"""
with open("app/templates/busca.html", "w", encoding="utf-8") as f:
    f.write(busca_html)
print("[ok] busca.html criado")

# ============ 5. ATUALIZA O BASE.HTML (Botão de busca no topo) ============
with open("app/templates/base.html", "r", encoding="utf-8") as f:
    base = f.read()

if '/buscar' not in base:
    base = base.replace(
        '<span class="brand-name">RASTREABILIDADE</span>',
        '<span class="brand-name">RASTREABILIDADE</span>\n            <a href="/buscar" class="top-search-btn">&#128269;</a>'
    )
    with open("app/templates/base.html", "w", encoding="utf-8") as f:
        f.write(base)
    print("[ok] base.html atualizado (botão de busca no topo)")

# ============ 6. NOVOS ESTILOS (O GRANDE DESIGN) ============
with open("app/static/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

if ".landing-hero" not in css:
    css += """

/* ===== LANDING PAGE (TELA INICIAL) ===== */
.landing-hero {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 70vh;
    text-align: center;
    padding: 20px;
}
.landing-content {
    max-width: 800px;
    width: 100%;
}
.landing-hero h1 {
    font-size: 56px;
    margin: 0 0 16px;
    letter-spacing: -2px;
    line-height: 1.1;
}
.landing-hero .subtitle {
    color: var(--text-dim);
    margin-bottom: 40px;
}

/* Barra de pesquisa estilosa */
.search-bar-wrapper {
    margin-bottom: 40px;
}
.search-bar {
    display: flex;
    align-items: center;
    background: var(--bg-elev);
    border: 2px solid var(--border);
    border-radius: 50px;
    padding: 8px 8px 8px 24px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    transition: border-color 0.3s, box-shadow 0.3s;
}
.search-bar:focus-within {
    border-color: var(--accent);
    box-shadow: 0 10px 30px rgba(249,115,22,0.2);
}
.search-icon {
    font-size: 20px;
    margin-right: 12px;
    color: var(--text-dim);
}
.search-bar input {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--text);
    font-size: 18px;
    padding: 12px 0;
    font-family: inherit;
}
.search-bar input:focus {
    outline: none;
}
.btn-search {
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 14px 32px;
    border-radius: 40px;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.2s, background 0.2s;
}
.btn-search:hover {
    transform: scale(1.05);
    background: #ea580c;
}

/* Links rápidos */
.quick-links {
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
}
.quick-link {
    padding: 10px 20px;
    background: var(--bg-elev);
    border: 1px solid var(--border);
    border-radius: 30px;
    color: var(--text-dim);
    text-decoration: none;
    font-size: 14px;
    transition: all 0.2s;
}
.quick-link:hover {
    border-color: var(--accent);
    color: var(--accent);
    transform: translateY(-2px);
}

/* Botão de busca no topo */
.top-search-btn {
    font-size: 18px;
    text-decoration: none;
    margin-left: 12px;
    opacity: 0.7;
    transition: opacity 0.2s;
}
.top-search-btn:hover { opacity: 1; }

/* Ajuste Mobile para a Landing Page */
@media (max-width: 600px) {
    .landing-hero h1 { font-size: 38px; }
    .search-bar { flex-direction: column; padding: 16px; border-radius: 16px; }
    .search-icon { display: none; }
    .search-bar input { width: 100%; text-align: center; margin-bottom: 12px; }
    .btn-search { width: 100%; }
}
"""
    with open("app/static/css/style.css", "w", encoding="utf-8") as f:
        f.write(css)
    print("[ok] CSS atualizado com o novo design (Landing Page + Busca)")

print("\nTUDO PRONTO! Reinicie o servidor e dê Ctrl+Shift+R no navegador.")
