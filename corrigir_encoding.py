# ============ 1. CORRIGE O BASE.HTML (força UTF-8 no navegador) ============
with open("app/templates/base.html", "r", encoding="utf-8") as f:
    base = f.read()

# Se ainda não tem a meta tag de charset, adiciona
if 'charset="UTF-8"' not in base and 'charset="utf-8"' not in base:
    base = base.replace(
        '<meta name="viewport"',
        '<meta charset="UTF-8">\n    <meta name="viewport"'
    )
    with open("app/templates/base.html", "w", encoding="utf-8") as f:
        f.write(base)
    print("[ok] base.html: meta charset adicionada")
else:
    print("[ok] base.html: meta charset j\u00e1 existia")

# ============ 2. REGRAVA O index.html COM ACENTOS CORRETOS ============
index_correto = '''{% extends "base.html" %}

{% block title %}In\u00edcio \u2014 Manual de Rastreabilidade{% endblock %}

{% block content %}
<section class="hero">
    <h1>Central de Consulta<span class="accent">.</span></h1>
    <p class="subtitle">Recebimento \u2014 Procedimentos, documentos e escala de abate.</p>
</section>

<section>
    <h2 class="section-title">Categorias</h2>
    <div class="grid">
        <a class="card" href="/categoria/operacoes">
            <span class="card-tag">Opera\u00e7\u00f5es</span>
            <h3>Procedimentos e tarefas</h3>
            <p>Consulta e organiza\u00e7\u00e3o das rotinas.</p>
        </a>
        <a class="card" href="/categoria/documentos">
            <span class="card-tag">Documentos</span>
            <h3>Exemplos de papeladas</h3>
            <p>Modelos e refer\u00eancias visuais.</p>
        </a>
        <a class="card" href="/categoria/escala">
            <span class="card-tag">Escala</span>
            <h3>Escala de abate</h3>
            <p>Montagem e sequ\u00eancia das opera\u00e7\u00f5es.</p>
        </a>
        <a class="card" href="/categoria/rastreio">
            <span class="card-tag">Rastreio</span>
            <h3>Brincos e identifica\u00e7\u00e3o</h3>
            <p>Orienta\u00e7\u00f5es de rastreabilidade animal.</p>
        </a>
    </div>
</section>

<section style="margin-top: 40px;">
    <h2 class="section-title">Procedimentos recentes</h2>
    <div class="grid">
        <a class="card" href="/tarefa/1">
            <span class="card-tag">Documentos</span>
            <h3>Confer\u00eancia de documentos ABCAR</h3>
            <p>Consulta de documentos e orienta\u00e7\u00f5es.</p>
        </a>
        <a class="card" href="/tarefa/2">
            <span class="card-tag">Escala</span>
            <h3>Montagem da escala de abate</h3>
            <p>Informa\u00e7\u00f5es e sequ\u00eancia das opera\u00e7\u00f5es.</p>
        </a>
    </div>
</section>
{% endblock %}
'''

with open("app/templates/index.html", "w", encoding="utf-8") as f:
    f.write(index_correto)
print("[ok] index.html regravado com UTF-8")

# ============ 3. CORRIGE O categoria.html (se tiver bugado) ============
cat_correto = '''{% extends "base.html" %}

{% block title %}{{ categoria.titulo }} \u2014 Manual de Rastreabilidade{% endblock %}

{% block content %}
<section class="hero">
    <a href="/" class="back-link">\u2190 Voltar</a>
    <h1>{{ categoria.titulo }}<span class="accent">.</span></h1>
    <p class="subtitle">{{ categoria.descricao }}</p>
</section>

<section>
    <h2 class="section-title">Procedimentos</h2>
    {% if procedimentos %}
    <div class="grid">
        {% for p in procedimentos %}
        <a class="card" href="/tarefa/{{ p.id }}">
            <span class="card-tag">{{ categoria.titulo }}</span>
            <h3>{{ p.titulo }}</h3>
            <p>{{ p.resumo }}</p>
        </a>
        {% endfor %}
    </div>
    {% else %}
    <p class="vazio">Nenhum procedimento cadastrado nesta categoria ainda.</p>
    {% endif %}
</section>
{% endblock %}
'''

with open("app/templates/categoria.html", "w", encoding="utf-8") as f:
    f.write(cat_correto)
print("[ok] categoria.html regravado com UTF-8")

print("\nPronto! Pode dar Ctrl+F5 no navegador.")
