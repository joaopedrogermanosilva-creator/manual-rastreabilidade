# ============ 1. ATUALIZA O FORM.HTML ============
with open("app/templates/form.html", "r", encoding="utf-8") as f:
    html = f.read()

# Adiciona o campo de upload ANTES do botão de salvar (se ainda não existir)
if 'name="arquivo"' not in html:
    campo_upload = """
    <div class="form-group">
        <label>Arquivo de Exemplo (PDF ou Imagem)</label>
        <input type="file" name="arquivo" accept=".pdf,image/*">
    </div>
"""
    html = html.replace('<div class="form-actions">', campo_upload + '\n    <div class="form-actions">')
    
    # Muda o enctype do form para aceitar arquivos
    html = html.replace('action="/tarefa/novo" method="POST"', 'action="/tarefa/novo" method="POST" enctype="multipart/form-data"')
    
    with open("app/templates/form.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[ok] form.html atualizado (campo de upload e enctype)")

# ============ 2. ATUALIZA O ROUTES.PY ============
with open("app/routes.py", "r", encoding="utf-8") as f:
    code = f.read()

# Adiciona imports necessários
code = code.replace(
    "from typing import Annotated",
    "from typing import Annotated\nfrom fastapi import UploadFile, File\nimport os\nfrom supabase_client import supabase"
)

# Substitui a rota POST /tarefa/novo
old_post = """@router.post("/tarefa/novo")
def salvar_novo(
    titulo: Annotated[str, Form()],
    categoria: Annotated[str, Form()],
    resumo: Annotated[str, Form()],
    objetivo: Annotated[str, Form()],
    como_realizar: Annotated[str, Form()],
    pontos_atencao: Annotated[str, Form()] = "",
):
    lista_passos = [p.strip() for p in como_realizar.strip().split("\\n") if p.strip()]
    lista_pontos = [p.strip() for p in pontos_atencao.strip().split("\\n") if p.strip()]

    novo_proc = {
        "categoria": categoria,
        "titulo": titulo,
        "resumo": resumo,
        "objetivo": objetivo,
        "como_realizar": lista_passos,
        "pontos_atencao": lista_pontos,
    }

    adicionar_procedimento(novo_proc)

    return RedirectResponse(url=f"/categoria/{categoria}", status_code=303)"""

new_post = """@router.post("/tarefa/novo")
def salvar_novo(
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

    arquivo_url = None
    if arquivo and arquivo.filename:
        # Faz o upload pro Supabase Storage
        conteudo = arquivo.file.read()
        path_no_bucket = f"procedimentos/{titulo.replace(' ', '_')}_{arquivo.filename}"
        
        try:
            supabase.storage.from_("documentos").upload(path_no_bucket, conteudo)
            # Pega a URL pública
            arquivo_url = supabase.storage.from_("documentos").get_public_url(path_no_bucket)
        except Exception as e:
            print(f"Erro no upload: {e}")

    novo_proc = {
        "categoria": categoria,
        "titulo": titulo,
        "resumo": resumo,
        "objetivo": objetivo,
        "como_realizar": lista_passos,
        "pontos_atencao": lista_pontos,
        "arquivo_url": arquivo_url,
    }

    adicionar_procedimento(novo_proc)

    return RedirectResponse(url=f"/categoria/{categoria}", status_code=303)"""

code = code.replace(old_post, new_post)

with open("app/routes.py", "w", encoding="utf-8") as f:
    f.write(code)
print("[ok] routes.py atualizado (upload)")

# ============ 3. ATUALIZA O dados.py ============
with open("app/dados.py", "r", encoding="utf-8") as f:
    dados = f.read()

# Adiciona o campo arquivo_url no dicionário de inserção
dados = dados.replace(
    '"pontos_atencao": novo_proc["pontos_atencao"],',
    '"pontos_atencao": novo_proc["pontos_atencao"],\n        "arquivo_url": novo_proc.get("arquivo_url"),'
)

with open("app/dados.py", "w", encoding="utf-8") as f:
    f.write(dados)
print("[ok] dados.py atualizado")

print("\\nTudo pronto! Reinicie o servidor e teste o upload.")
