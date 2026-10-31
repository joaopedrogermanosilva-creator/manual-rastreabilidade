import os

# ============ 1. ATUALIZA BASE.HTML (Ícones Modernos) ============
with open("app/templates/base.html", "r", encoding="utf-8") as f:
    html = f.read()

# Adiciona os ícones do Phosphor no Head
if "phosphor-icons" not in html:
    html = html.replace("</head>", '    <script src="https://unpkg.com/@phosphor-icons/web"></script>\n</head>')

# Troca o menu do sidebar para usar os novos ícones
html = html.replace('<li><a href="/">&#127968; Início</a></li>', '<li><a href="/"><i class="ph ph-house"></i> Início</a></li>')
html = html.replace('&#128196; {{ cat.titulo }}', '<i class="ph ph-folder-open"></i> {{ cat.titulo }}')
html = html.replace('<span class="brand-mark">&#9684;&#9682;</span>', '<span class="brand-mark"><i class="ph ph-crosshair"></i></span>')
html = html.replace('<span class="theme-icon">&#9680;</span>', '<span class="theme-icon"><i class="ph ph-moon"></i></span>')

with open("app/templates/base.html", "w", encoding="utf-8") as f:
    f.write(html)
print("[ok] base.html atualizado com Phosphor Icons")

# ============ 2. ATUALIZA TAREFA.HTML (Design dos Passos e Upload) ============
tarefa_html = """{% extends "base.html" %}
{% block title %}{{ proc.titulo }} &mdash; Manual de Rastreabilidade{% endblock %}

{% block content %}
<section class="hero">
    <a href="/categoria/{{ proc.categoria_slug }}" class="back-link"><i class="ph ph-arrow-left"></i> Voltar para {{ categoria.titulo }}</a>
    <h1>{{ proc.titulo }}<span class="accent">.</span></h1>
    <p class="subtitle">{{ proc.resumo }}</p>

    <div class="acoes-tarefa">
        <a href="/tarefa/{{ proc.id }}/editar" class="btn-editar"><i class="ph ph-pencil-simple"></i> Editar</a>
        <form action="/tarefa/{{ proc.id }}/excluir" method="POST" style="display:inline;" onsubmit="return confirm('Excluir este procedimento?');">
            <button type="submit" class="btn-excluir"><i class="ph ph-trash"></i> Excluir</button>
        </form>
    </div>
</section>

<section class="bloco">
    <h2 class="section-title"><i class="ph ph-target"></i> 1. Objetivo da tarefa</h2>
    <p>{{ proc.objetivo }}</p>
</section>

<section class="bloco">
    <h2 class="section-title"><i class="ph ph-list-checks"></i> 2. Como realizar</h2>
    <div class="passos-grid">
        {% for passo in proc.como_realizar %}
        <div class="passo-card">
            <span class="passo-num">{{ loop.index }}</span>
            <p>{{ passo }}</p>
        </div>
        {% endfor %}
    </div>
</section>

<section class="bloco">
    <h2 class="section-title"><i class="ph ph-warning-circle"></i> 3. Pontos de atenção</h2>
    <ul class="atencao">
        {% for ponto in proc.pontos_atencao %}
        <li>{{ ponto }}</li>
        {% endfor %}
    </ul>
</section>

<section class="bloco">
    <h2 class="section-title"><i class="ph ph-paperclip"></i> 4. Exemplos de documentos</h2>
    {% if proc.arquivo_url %}
        <div class="arquivo-card">
            {% if proc.arquivo_url.endswith('.pdf') %}
                <i class="ph ph-file-pdf" style="font-size: 48px; color: #dc2626;"></i>
                <h3>Documento PDF</h3>
                <a href="{{ proc.arquivo_url }}" target="_blank" class="btn-primary"><i class="ph ph-download-simple"></i> Abrir PDF</a>
            {% else %}
                <img src="{{ proc.arquivo_url }}" alt="Exemplo" style="width:100%; max-width: 500px; border-radius:8px; margin-bottom: 16px;">
            {% endif %}
        </div>
    {% else %}
        <p class="aviso-fase"><i class="ph ph-info"></i> Nenhum arquivo anexado a este procedimento.</p>
    {% endif %}
</section>
{% endblock %}
"""
with open("app/templates/tarefa.html", "w", encoding="utf-8") as f:
    f.write(tarefa_html)
print("[ok] tarefa.html atualizado com design moderno")

# ============ 3. ATUALIZA BUSCA.HTML ============
busca_html = """{% extends "base.html" %}
{% block title %}Resultados da busca{% endblock %}
{% block content %}
<section class="hero">
    <a href="/" class="back-link"><i class="ph ph-arrow-left"></i> Voltar para o início</a>
    <h1>Resultados para: <span class="accent">"{{ termo }}"</span></h1>
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
    <div class="empty-state">
        <i class="ph ph-magnifying-glass"></i>
        <h3>Nenhum resultado encontrado</h3>
        <p>Tente pesquisar por outro termo.</p>
    </div>
    {% endif %}
</section>
{% endblock %}
"""
with open("app/templates/busca.html", "w", encoding="utf-8") as f:
    f.write(busca_html)
print("[ok] busca.html atualizado")

# ============ 4. ATUALIZA O CSS ============
css_extra = """

/* ===== ÍCONES E DESIGN DOS PASSOS ===== */
.section-title i {
    font-size: 20px;
    margin-right: 8px;
    color: var(--accent);
}
.passos-grid {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 16px;
}
.passo-card {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    background: var(--bg);
    padding: 16px;
    border-radius: 8px;
    border: 1px solid var(--border);
    transition: transform 0.2s;
}
.passo-card:hover {
    transform: translateX(4px);
    border-color: var(--accent);
}
.passo-num {
    background: var(--accent);
    color: #fff;
    font-weight: bold;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    flex-shrink: 0;
}
.passo-card p {
    margin: 0;
    color: var(--text);
    line-height: 1.5;
}
.arquivo-card {
    background: var(--bg);
    padding: 24px;
    border-radius: 8px;
    border: 1px dashed var(--border);
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
}
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-dim);
}
.empty-state i {
    font-size: 64px;
    margin-bottom: 16px;
    color: var(--border);
}
"""
with open("app/static/css/style.css", "a", encoding="utf-8") as f:
    f.write(css_extra)
print("[ok] CSS atualizado com novos estilos")

print("\nTUDO PRONTO! Agora envie para o Render.")
