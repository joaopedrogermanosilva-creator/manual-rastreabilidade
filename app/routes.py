from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from supabase_client import supabase

from app.dados import (
    buscar_procedimento, adicionar_procedimento, atualizar_procedimento,
    excluir_procedimento, get_categorias, get_procedimentos_por_categoria, buscar_procedimentos,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html",
        context={"categorias": get_categorias()},
    )




@router.get("/buscar", response_class=HTMLResponse)
def buscar(request: Request, q: str = ""):
    resultados = buscar_procedimentos(q) if q else []
    return templates.TemplateResponse(
        request=request, name="busca.html",
        context={"resultados": resultados, "termo": q, "categorias": get_categorias()},
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
    lista_passos = [p.strip() for p in como_realizar.strip().split("\n") if p.strip()]
    lista_pontos = [p.strip() for p in pontos_atencao.strip().split("\n") if p.strip()]
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
    lista_passos = [p.strip() for p in como_realizar.strip().split("\n") if p.strip()]
    lista_pontos = [p.strip() for p in pontos_atencao.strip().split("\n") if p.strip()]
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
