# 1. FORMULÁRIO NOVO (Com Upload)
form_novo = """{% extends "base.html" %}
{% block title %}Novo Procedimento{% endblock %}
{% block content %}
<section class="hero">
    <a href="/" class="back-link"><i class="ph ph-arrow-left"></i> Voltar</a>
    <h1>Novo Procedimento<span class="accent">.</span></h1>
</section>
<form action="/tarefa/novo" method="POST" class="form-manual" enctype="multipart/form-data">
    <div class="form-group"><label>Título</label><input type="text" name="titulo" required></div>
    <div class="form-group"><label>Categoria</label><select name="categoria" required><option value="">Selecione...</option>{% for slug, cat in categorias.items() %}<option value="{{ slug }}">{{ cat.titulo }}</option>{% endfor %}</select></div>
    <div class="form-group"><label>Resumo Curto</label><input type="text" name="resumo" required></div>
    <div class="form-group"><label>Objetivo</label><textarea name="objetivo" rows="3" required></textarea></div>
    <div class="form-group"><label>Como realizar (um passo por linha)</label><textarea name="como_realizar" rows="5" required></textarea></div>
    <div class="form-group"><label>Pontos de atenção (um por linha)</label><textarea name="pontos_atencao" rows="3"></textarea></div>
    <div class="form-group"><label>Anexar Imagem ou PDF</label><input type="file" name="arquivo" accept=".pdf,image/*"></div>
    <div class="form-actions"><a href="/" class="btn-cancel">Cancelar</a><button type="submit" class="btn-primary"><i class="ph ph-floppy-disk"></i> Salvar</button></div>
</form>
{% endblock %}"""
with open("app/templates/form.html", "w", encoding="utf-8") as f: f.write(form_novo)
print("[ok] form.html atualizado")

# 2. FORMULÁRIO EDITAR (Com Upload)
form_editar = """{% extends "base.html" %}
{% block title %}Editar: {{ proc.titulo }}{% endblock %}
{% block content %}
<section class="hero">
    <a href="/tarefa/{{ proc.id }}" class="back-link"><i class="ph ph-arrow-left"></i> Voltar</a>
    <h1>Editar Procedimento<span class="accent">.</span></h1>
</section>
<form action="/tarefa/{{ proc.id }}/editar" method="POST" class="form-manual" enctype="multipart/form-data">
    <div class="form-group"><label>Título</label><input type="text" name="titulo" required value="{{ proc.titulo }}"></div>
    <div class="form-group"><label>Categoria</label><select name="categoria" required>{% for slug, cat in categorias.items() %}<option value="{{ slug }}" {% if slug == proc.categoria_slug %}selected{% endif %}>{{ cat.titulo }}</option>{% endfor %}</select></div>
    <div class="form-group"><label>Resumo Curto</label><input type="text" name="resumo" required value="{{ proc.resumo }}"></div>
    <div class="form-group"><label>Objetivo</label><textarea name="objetivo" rows="3" required>{{ proc.objetivo }}</textarea></div>
    <div class="form-group"><label>Como realizar</label><textarea name="como_realizar" rows="5" required>{{ proc.como_realizar | join('\n') }}</textarea></div>
    <div class="form-group"><label>Pontos de atenção</label><textarea name="pontos_atencao" rows="3">{{ proc.pontos_atencao | join('\n') }}</textarea></div>
    <div class="form-group">
        <label>Anexar Imagem ou PDF</label>
        {% if proc.arquivo_url %}<p style="font-size:12px;">Atual: <a href="{{ proc.arquivo_url }}" target="_blank">Ver arquivo</a></p>{% endif %}
        <input type="file" name="arquivo" accept=".pdf,image/*">
    </div>
    <div class="form-actions"><a href="/tarefa/{{ proc.id }}" class="btn-cancel">Cancelar</a><button type="submit" class="btn-primary"><i class="ph ph-floppy-disk"></i> Salvar</button></div>
</form>
{% endblock %}"""
with open("app/templates/form_editar.html", "w", encoding="utf-8") as f: f.write(form_editar)
print("[ok] form_editar.html atualizado")

# 3. ROUTES.PY COMPLETO (Com lógica de upload blindada)
routes = """from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from supabase_client import supabase
from app.dados import (buscar_procedimento, adicionar_procedimento, atualizar_procedimento, excluir_procedimento, get_categorias, get_procedimentos_por_categoria, buscar_procedimentos)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"categorias": get_categorias()})

@router.get("/categoria/{slug}", response_class=HTMLResponse)
def categoria(slug: str, request: Request):
    cats = get_categorias()
    if slug not in cats: raise HTTPException(404)
    return templates.TemplateResponse(request=request, name="categoria.html", context={"categoria": cats[slug], "categoria_slug": slug, "procedimentos": get_procedimentos_por_categoria(slug), "categorias": cats})

@router.get("/buscar", response_class=HTMLResponse)
def buscar(request: Request, q: str = ""):
    return templates.TemplateResponse(request=request, name="busca.html", context={"resultados": buscar_procedimentos(q) if q else [], "termo": q, "categorias": get_categorias()})

@router.get("/tarefa/novo", response_class=HTMLResponse)
def form_novo(request: Request):
    return templates.TemplateResponse(request=request, name="form.html", context={"categorias": get_categorias()})

@router.post("/tarefa/novo")
def salvar_novo(titulo: Annotated[str, Form()], categoria: Annotated[str, Form()], resumo: Annotated[str, Form()], objetivo: Annotated[str, Form()], como_realizar: Annotated[str, Form()], pontos_atencao: Annotated[str, Form()] = "", arquivo: UploadFile = File(None)):
    passos = [p.strip() for p in como_realizar.strip().split("\\n") if p.strip()]
    pontos = [p.strip() for p in pontos_atencao.strip().split("\\n") if p.strip()]
    url = None
    if arquivo and arquivo.filename:
        try:
            path = f"proc_{titulo.replace(' ', '_')}_{arquivo.filename}"
            supabase.storage.from_("documentos").upload(path, arquivo.file.read())
            url = supabase.storage.from_("documentos").get_public_url(path)
        except Exception as e: print(f"Erro Upload: {e}")
    adicionar_procedimento({"categoria": categoria, "titulo": titulo, "resumo": resumo, "objetivo": objetivo, "como_realizar": passos, "pontos_atencao": pontos, "arquivo_url": url})
    return RedirectResponse(f"/categoria/{categoria}", 303)

@router.get("/tarefa/{proc_id}/editar", response_class=HTMLResponse)
def form_editar(proc_id: int, request: Request):
    proc = buscar_procedimento(proc_id)
    if not proc: raise HTTPException(404)
    return templates.TemplateResponse(request=request, name="form_editar.html", context={"proc": proc, "categorias": get_categorias()})

@router.post("/tarefa/{proc_id}/editar")
def salvar_edicao(proc_id: int, titulo: Annotated[str, Form()], categoria: Annotated[str, Form()], resumo: Annotated[str, Form()], objetivo: Annotated[str, Form()], como_realizar: Annotated[str, Form()], pontos_atencao: Annotated[str, Form()] = "", arquivo: UploadFile = File(None)):
    passos = [p.strip() for p in como_realizar.strip().split("\\n") if p.strip()]
    pontos = [p.strip() for p in pontos_atencao.strip().split("\\n") if p.strip()]
    url = buscar_procedimento(proc_id).get("arquivo_url")
    if arquivo and arquivo.filename:
        try:
            path = f"proc_{titulo.replace(' ', '_')}_{arquivo.filename}"
            supabase.storage.from_("documentos").upload(path, arquivo.file.read(), {"upsert": "true"})
            url = supabase.storage.from_("documentos").get_public_url(path)
        except Exception as e: print(f"Erro Upload: {e}")
    atualizar_procedimento(proc_id, {"categoria": categoria, "titulo": titulo, "resumo": resumo, "objetivo": objetivo, "como_realizar": passos, "pontos_atencao": pontos, "arquivo_url": url})
    return RedirectResponse(f"/tarefa/{proc_id}", 303)

@router.post("/tarefa/{proc_id}/excluir")
def excluir(proc_id: int):
    proc = buscar_procedimento(proc_id)
    if proc: excluir_procedimento(proc_id); return RedirectResponse(f"/categoria/{proc['categoria_slug']}", 303)
    raise HTTPException(404)

@router.get("/tarefa/{proc_id}", response_class=HTMLResponse)
def tarefa(proc_id: int, request: Request):
    proc = buscar_procedimento(proc_id)
    if not proc: raise HTTPException(404)
    cats = get_categorias()
    return templates.TemplateResponse(request=request, name="tarefa.html", context={"proc": proc, "categoria": cats.get(proc["categoria_slug"], {"titulo": ""}), "categorias": cats})
"""
with open("app/routes.py", "w", encoding="utf-8") as f: f.write(routes)
print("[ok] routes.py reescrito do zero")
