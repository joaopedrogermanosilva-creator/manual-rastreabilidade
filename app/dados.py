from supabase_client import supabase

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
    }
    response = supabase.table("procedimentos").update(dados_para_atualizar).eq("id", proc_id).execute()
    return response.data[0] if response.data else None

def excluir_procedimento(proc_id):
    supabase.table("procedimentos").delete().eq("id", proc_id).execute()


def buscar_procedimentos(termo):
    """Busca global usando ilike no Supabase."""
    if not termo:
        return []
    # O Supabase permite busca com .or_ para verificar múltiplas colunas
    response = supabase.table("procedimentos").select("*").or_(
        f"titulo.ilike.%{termo}%,resumo.ilike.%{termo}%,objetivo.ilike.%{termo}%"
    ).execute()
    return response.data
