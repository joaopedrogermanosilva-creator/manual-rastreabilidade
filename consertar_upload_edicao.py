# ============ 1. ATUALIZA O FORM_EDITAR.HTML (campo de upload) ============
form_editar_html = """{% extends "base.html" %}

{% block title %}Editar: {{ proc.titulo }}{% endblock %}

{% block content %}
<section class="hero">
    <a href="/tarefa/{{ proc.id }}" class="back-link">&#8592; Voltar para a tarefa</a>
    <h1>Editar Procedimento<span class="accent">.</span></h1>
    <p class="subtitle">{{ proc.titulo }}</p>
</section>

<form action="/tarefa/{{ proc.id }}/editar" method="POST" class="form-manual" enctype="multipart/form-data">
    <div class="form-group">
        <label>T&#237;tulo do Procedimento</label>
        <input type="text" name="titulo" required value="{{ proc.titulo }}">
    </div>

    <div class="form-group">
        <label>Categoria</label>
        <select name="categoria" required>
            {% for slug, cat in categorias.items() %}
            <option value="{{ slug }}" {% if slug == proc.categoria_slug %}selected{% endif %}>{{ cat.titulo }}</option>
            {% endfor %}
        </select>
    </div>

    <div class="form-group">
        <label>Resumo Curto</label>
        <input type="text" name="resumo" required value="{{ proc.resumo }}">
    </div>

    <div class="form-group">
        <label>Objetivo da tarefa</label>
        <textarea name="objetivo" rows="3" required>{{ proc.objetivo }}</textarea>
    </div>

    <div class="form-group">
        <label>Como realizar (um passo por linha)</label>
        <textarea name="como_realizar" rows="5" required>{{ proc.como_realizar | join('\n') }}</textarea>
    </div>

    <div class="form-group">
        <label>Pontos de aten&#231;&#227;o (um por linha)</label>
        <textarea name="pontos_atencao" rows="3">{{ proc.pontos_atencao | join('\n') }}</textarea>
    </div>

    <div class="form-group">
        <label>Arquivo de Exemplo (PDF ou Imagem)</label>
        {% if proc.arquivo_url %}
            <p style="font-size:12px; color:var(--text-dim); margin-bottom:8px;">Arquivo atual: <a href="{{ proc.arquivo_url }}" target="_blank">Ver arquivo</a></p>
        {% endif %}
        <input type="file" name="arquivo" accept=".pdf,image/*">
        <p style="font-size:12px; color:var(--text-dim); margin-top:4px;">Deixe em branco para manter o arquivo atual.</p>
    </div>

    <div class="form-actions">
        <a href="/tarefa/{{ proc.id }}" class="btn-cancel">Cancelar</a>
        <button type="submit" class="btn-primary">Salvar Altera&#231;&#245;es</button>
    </div>
</form>
{% endblock %}
"""

with open("app/templates/form_editar.html", "w", encoding="utf-8") as f:
    f.write(form_editar_html)
print("[ok] form_editar.html atualizado (campo de upload)")

# ============ 2. ATUALIZA ROUTES.PY (upload na edição) ============
with open("app/routes.py", "r", encoding="utf-8") as f:
    code = f.read()

# Substitui a rota POST de edição
old_edit = """@router.post("/tarefa/{proc_id}/editar")
def salvar_edicao(
    proc_id: int,
    titulo: Annotated[str, Form()],
    categoria: Annotated[str, Form()],
    resumo: Annotated[str, Form()],
    objetivo: Annotated[str, Form()],
    como_realizar: Annotated[str, Form()],
    pontos_atencao: Annotated[str, Form()] = "",
):
    lista_passos = [p.strip() for p in como_realizar.strip().split("\\n") if p.strip()]
    lista_pontos = [p.strip() for p in pontos_atencao.strip().split("\\n") if p.strip()]

    atualizar_procedimento(proc_id, {
        "categoria": categoria,
        "titulo": titulo,
        "resumo": resumo,
        "objetivo": objetivo,
        "como_realizar": lista_passos,
        "pontos_atencao": lista_pontos,
    })
    return RedirectResponse(url=f"/tarefa/{proc_id}", status_code=303)"""

new_edit = """@router.post("/tarefa/{proc_id}/editar")
def salvar_edicao(
    proc_id: int,
    titulo: Annotated[str, Form()],
    categoria: Annotated[str, Form()],
    resumo: Annotated[str, Form()],
    objetivo: Annotated[str, Form()],
    como_realizar: Annotated[str, Form()],
    pontos_atencao: Annotated[str, Form()] = "",
    arquivo: UploadFile = File(None),
):
    lista_passos = [p.strip() for p in como_realizar.strip().split("\\n") if p.strip()]
    lista_pontos = [p.strip() for p in pontos_atencao.strip().split("\\n") if p.strip()]

    # Mantém o arquivo atual por padrão
    proc_atual = buscar_procedimento(proc_id)
    arquivo_url = proc_atual.get("arquivo_url") if proc_atual else None

    if arquivo and arquivo.filename:
        conteudo = arquivo.file.read()
        path_no_bucket = f"procedimentos/{titulo.replace(' ', '_')}_{arquivo.filename}"
        try:
            supabase.storage.from_("documentos").upload(path_no_bucket, conteudo, {"upsert": "true"})
            arquivo_url = supabase.storage.from_("documentos").get_public_url(path_no_bucket)
        except Exception as e:
            print(f"Erro no upload: {e}")

    atualizar_procedimento(proc_id, {
        "categoria": categoria,
        "titulo": titulo,
        "resumo": resumo,
        "objetivo": objetivo,
        "como_realizar": lista_passos,
        "pontos_atencao": lista_pontos,
        "arquivo_url": arquivo_url,
    })
    return RedirectResponse(url=f"/tarefa/{proc_id}", status_code=303)"""

code = code.replace(old_edit, new_edit)

# Corrige o import do UploadFile se não tiver
if "from fastapi import UploadFile, File" not in code:
    code = code.replace(
        "from fastapi import APIRouter, HTTPException, Request, Form",
        "from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File"
    )

with open("app/routes.py", "w", encoding="utf-8") as f:
    f.write(code)
print("[ok] routes.py atualizado (upload na edição)")

print("\nTudo pronto! O uvicorn vai reiniciar sozinho. Dê Ctrl+F5 no navegador.")
