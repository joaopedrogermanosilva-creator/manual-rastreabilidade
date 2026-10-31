import os

# ============ 1. CORRIGE O BOTÃO VOLTAR NO TAREFA.HTML E MOSTRA A IMAGEM ============
tarefa_html = """{% extends "base.html" %}

{% block title %}{{ proc.titulo }} &mdash; Manual de Rastreabilidade{% endblock %}

{% block content %}
<section class="hero">
    <a href="/categoria/{{ proc.categoria_slug }}" class="back-link">&#8592; Voltar para {{ categoria.titulo }}</a>
    <h1>{{ proc.titulo }}<span class="accent">.</span></h1>
    <p class="subtitle">{{ proc.resumo }}</p>

    <div class="acoes-tarefa">
        <a href="/tarefa/{{ proc.id }}/editar" class="btn-editar">&#9998; Editar</a>
        <form action="/tarefa/{{ proc.id }}/excluir" method="POST" style="display:inline;" onsubmit="return confirm('Excluir este procedimento?');">
            <button type="submit" class="btn-excluir">&#10006; Excluir</button>
        </form>
    </div>
</section>

<section class="bloco">
    <h2 class="section-title">1. Objetivo da tarefa</h2>
    <p>{{ proc.objetivo }}</p>
</section>

<section class="bloco">
    <h2 class="section-title">2. Como realizar</h2>
    <ol class="passos">
        {% for passo in proc.como_realizar %}
        <li>{{ passo }}</li>
        {% endfor %}
    </ol>
</section>

<section class="bloco">
    <h2 class="section-title">3. Pontos de atenção</h2>
    <ul class="atencao">
        {% for ponto in proc.pontos_atencao %}
        <li>{{ ponto }}</li>
        {% endfor %}
    </ul>
</section>

<section class="bloco">
    <h2 class="section-title">4. Exemplos de documentos</h2>
    {% if proc.arquivo_url %}
        <div class="card exemplo" style="max-width: 400px;">
            <span class="card-tag">Arquivo</span>
            {% if proc.arquivo_url.endswith('.pdf') %}
                <h3>&#128196; PDF Anexado</h3>
                <a href="{{ proc.arquivo_url }}" target="_blank" class="btn-primary" style="text-decoration:none; display:inline-block; margin-top:10px;">Abrir PDF</a>
            {% else %}
                <img src="{{ proc.arquivo_url }}" alt="Exemplo" style="width:100%; border-radius:6px; margin-top:10px;">
            {% endif %}
        </div>
    {% else %}
        <p class="aviso-fase">Nenhum arquivo anexado a este procedimento.</p>
    {% endif %}
</section>
{% endblock %}
"""

with open("app/templates/tarefa.html", "w", encoding="utf-8") as f:
    f.write(tarefa_html)
print("[ok] tarefa.html atualizado (voltar + imagem)")


# ============ 2. DEIXA O DESIGN MAIS BONITO (CSS) ============
css_extra = """

/* ===== DESIGN MELHORADO ===== */
.topbar {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    backdrop-filter: blur(8px);
    background: rgba(23, 23, 27, 0.85) !important;
}
[data-theme="light"] .topbar {
    background: rgba(255,255,255,0.85) !important;
}

.hero {
    padding: 20px 0 10px;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    left: -24px;
    top: 20px;
    width: 4px;
    height: 40px;
    background: var(--accent);
    border-radius: 2px;
}

.card {
    position: relative;
    overflow: hidden;
}
.card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 8px;
    padding: 1px;
    background: linear-gradient(135deg, transparent, transparent);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
    transition: background 0.3s;
}
.card:hover::after {
    background: linear-gradient(135deg, var(--accent), transparent);
}

.bloco {
    position: relative;
    transition: transform 0.2s, box-shadow 0.2s;
}
.bloco:hover {
    transform: translateX(4px);
    box-shadow: -4px 0 0 0 var(--accent);
}

.acoes-tarefa {
    margin-top: 20px;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.btn-editar, .btn-excluir {
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    border: 1px solid var(--border);
    background: var(--bg-elev);
    color: var(--text);
    transition: all 0.2s;
    font-family: inherit;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.btn-editar:hover {
    border-color: var(--accent);
    color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(249,115,22,0.2);
}
.btn-excluir:hover {
    border-color: #dc2626;
    color: #dc2626;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(220,38,38,0.2);
}

/* Ícones nos títulos de seção */
.section-title::before {
    content: '';
    display: inline-block;
    width: 8px;
    height: 8px;
    background: var(--accent);
    border-radius: 50%;
    margin-right: 8px;
    vertical-align: middle;
}

/* Scrollbar bonita */
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
"""

with open("app/static/css/style.css", "a", encoding="utf-8") as f:
    f.write(css_extra)
print("[ok] CSS atualizado (design melhorado)")

print("\nTudo pronto! O uvicorn vai reiniciar sozinho. Dê Ctrl+F5 no navegador.")
