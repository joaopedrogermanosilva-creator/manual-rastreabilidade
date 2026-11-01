from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from uuid import UUID
from supabase_client import supabase
from app.dados import (buscar_procedimento, adicionar_procedimento, atualizar_procedimento, excluir_procedimento, get_categorias, get_procedimentos_por_categoria, buscar_procedimentos)
from app.dados_pastas import (
    buscar_pasta,
    listar_opcoes_pasta,
    listar_pastas,
    listar_procedimentos_da_pasta,
    obter_breadcrumb,
)

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

@router.get("/pastas", response_class=HTMLResponse)
def pastas_raiz(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pasta.html",
        context={
            "categorias": get_categorias(),
            "pasta": None,
            "breadcrumb": [],
            "subpastas": listar_pastas(),
            "procedimentos": [],
        },
    )

@router.get("/pasta/{pasta_id}", response_class=HTMLResponse)
def pasta(pasta_id: UUID, request: Request):
    pasta_atual = buscar_pasta(pasta_id)
    if not pasta_atual:
        raise HTTPException(404)
    return templates.TemplateResponse(
        request=request,
        name="pasta.html",
        context={
            "categorias": get_categorias(),
            "pasta": pasta_atual,
            "breadcrumb": obter_breadcrumb(pasta_id),
            "subpastas": listar_pastas(pasta_id),
            "procedimentos": listar_procedimentos_da_pasta(pasta_id),
        },
    )

@router.get("/tarefa/novo", response_class=HTMLResponse)
def form_novo(request: Request):
    return templates.TemplateResponse(request=request, name="form.html", context={"categorias": get_categorias(), "pastas": listar_opcoes_pasta()})

@router.post("/tarefa/novo")
def salvar_novo(titulo: Annotated[str, Form()], categoria: Annotated[str, Form()], resumo: Annotated[str, Form()], objetivo: Annotated[str, Form()], como_realizar: Annotated[str, Form()], pontos_atencao: Annotated[str, Form()] = "", pasta_id: Annotated[str | None, Form()] = None, arquivo: UploadFile = File(None)):
    pasta_id_validado = _validar_pasta_id(pasta_id)
    passos = [p.strip() for p in como_realizar.strip().split("\n") if p.strip()]
    pontos = [p.strip() for p in pontos_atencao.strip().split("\n") if p.strip()]
    url = None
    if arquivo and arquivo.filename:
        try:
            path = f"proc_{titulo.replace(' ', '_')}_{arquivo.filename}"
            supabase.storage.from_("documentos").upload(path, arquivo.file.read())
            url = supabase.storage.from_("documentos").get_public_url(path)
        except Exception as e: print(f"Erro Upload: {e}")
    adicionar_procedimento({"categoria": categoria, "titulo": titulo, "resumo": resumo, "objetivo": objetivo, "como_realizar": passos, "pontos_atencao": pontos, "arquivo_url": url, "pasta_id": pasta_id_validado})
    if pasta_id_validado:
        return RedirectResponse(f"/pasta/{pasta_id_validado}", 303)
    return RedirectResponse(f"/categoria/{categoria}", 303)

@router.get("/tarefa/{proc_id}/editar", response_class=HTMLResponse)
def form_editar(proc_id: int, request: Request):
    proc = buscar_procedimento(proc_id)
    if not proc: raise HTTPException(404)
    return templates.TemplateResponse(request=request, name="form_editar.html", context={"proc": proc, "categorias": get_categorias(), "pastas": listar_opcoes_pasta()})

@router.post("/tarefa/{proc_id}/editar")
def salvar_edicao(proc_id: int, titulo: Annotated[str, Form()], categoria: Annotated[str, Form()], resumo: Annotated[str, Form()], objetivo: Annotated[str, Form()], como_realizar: Annotated[str, Form()], pontos_atencao: Annotated[str, Form()] = "", pasta_id: Annotated[str | None, Form()] = None, arquivo: UploadFile = File(None)):
    passos = [p.strip() for p in como_realizar.strip().split("\n") if p.strip()]
    pontos = [p.strip() for p in pontos_atencao.strip().split("\n") if p.strip()]
    proc_atual = buscar_procedimento(proc_id)
    if not proc_atual:
        raise HTTPException(404)
    pasta_id_validado = (
        _validar_pasta_id(pasta_id)
        if pasta_id is not None
        else proc_atual.get("pasta_id")
    )
    url = proc_atual.get("arquivo_url") if proc_atual else None
    if arquivo and arquivo.filename:
        try:
            path = f"proc_{titulo.replace(' ', '_')}_{arquivo.filename}"
            supabase.storage.from_("documentos").upload(path, arquivo.file.read(), {"upsert": "true"})
            url = supabase.storage.from_("documentos").get_public_url(path)
        except Exception as e: print(f"Erro Upload: {e}")
    atualizar_procedimento(proc_id, {"categoria": categoria, "titulo": titulo, "resumo": resumo, "objetivo": objetivo, "como_realizar": passos, "pontos_atencao": pontos, "arquivo_url": url, "pasta_id": pasta_id_validado})
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

def _validar_pasta_id(pasta_id: str | None):
    if not pasta_id or pasta_id == "__none__":
        return None
    try:
        pasta_uuid = UUID(pasta_id)
    except ValueError as exc:
        raise HTTPException(400, "Identificador de pasta inválido.") from exc
    if not buscar_pasta(pasta_uuid):
        raise HTTPException(400, "A pasta selecionada não existe.")
    return str(pasta_uuid)
