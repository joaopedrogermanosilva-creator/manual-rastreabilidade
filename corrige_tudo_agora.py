import os

# ============ 1. ARQUIVO DE DADOS CORRETO ============
dados_py = """from supabase_client import supabase

def get_categorias():
    response = supabase.table("categorias").select("*").execute()
    return {c["slug"]: {"titulo": c["titulo"], "descricao": c["descricao"]} for c in response.data}

def get_procedimentos_por_categoria(slug):
    response = supabase.table("procedimentos").select("*").eq("categoria_slug", slug).execute()
    return response.data

def buscar_procedimento(proc_id):
    response = supabase.table("procedimentos").select("*").eq("id", proc_id).execute()
    return response.data[0] if response.data else None

def adicionar_procedimento(novo_proc):
    dados_para_inserir = {
        "categoria_slug": novo_proc["categoria"],
        "titulo": novo_proc["titulo"],
        "resumo": novo_proc["resumo"],
        "objetivo": novo_proc["objetivo"],
        "como_realizar": novo_proc["como_realizar"],
        "pontos_atencao": novo_proc["pontos_atencao"],
        "arquivo_url": novo_proc.get("arquivo_url"),
    }
    response = supabase.table("procedimentos").insert(dados_para_inserir).execute()
    return response.data[0] if response.data else None

def atualizar_procedimento(proc_id, novos_dados):
    dados_para_atualizar = {
        "categoria_slug": novos_dados["categoria"],
        "titulo": novos_dados["titulo"],
        "resumo": novos_dados["resumo"],
        "objetivo": novos_dados["objetivo"],
        "como_realizar": novos_dados["como_realizar"],
        "pontos_atencao": novos_dados["pontos_atencao"],
        "arquivo_url": novos_dados.get("arquivo_url"),
    }
    response = supabase.table("procedimentos").update(dados_para_atualizar).eq("id", proc_id).execute()
    return response.data[0] if response.data else None

def excluir_procedimento(proc_id):
    supabase.table("procedimentos").delete().eq("id", proc_id).execute()

def buscar_procedimentos(termo):
    if not termo: return []
    response = supabase.table("procedimentos").select("*").or_(
        f"titulo.ilike.%{termo}%,resumo.ilike.%{termo}%,objetivo.ilike.%{termo}%"
    ).execute()
    return response.data
"""

with open("app/dados.py", "w", encoding="utf-8") as f:
    f.write(dados_py)
print("[ok] app/dados.py reescrito com correção de upload")

# ============ 2. ROTAS CORRETAS ============
routes_py = """from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File
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
    proc_atual = buscar_procedimento(proc_id)
    url = proc_atual.get("arquivo_url") if proc_atual else None
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
    if proc:
        excluir_procedimento(proc_id)
        return RedirectResponse(f"/categoria/{proc['categoria_slug']}", 303)
    raise HTTPException(404)

@router.get("/tarefa/{proc_id}", response_class=HTMLResponse)
def tarefa(proc_id: int, request: Request):
    proc = buscar_procedimento(proc_id)
    if not proc: raise HTTPException(404)
    cats = get_categorias()
    return templates.TemplateResponse(request=request, name="tarefa.html", context={"proc": proc, "categoria": cats.get(proc["categoria_slug"], {"titulo": ""}), "categorias": cats})
"""

with open("app/routes.py", "w", encoding="utf-8") as f:
    f.write(routes_py)
print("[ok] app/routes.py reescrito com correção de upload")
