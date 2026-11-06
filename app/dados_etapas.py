from supabase_client import supabase


def buscar_etapas(procedimento_id: int) -> list[dict]:
    response = (
        supabase.table("etapas")
        .select("*")
        .eq("procedimento_id", procedimento_id)
        .order("ordem")
        .execute()
    )
    return response.data


def adicionar_etapas(procedimento_id: int, etapas: list[dict]) -> list[dict]:
    if not etapas:
        return []

    registros = [
        {
            "procedimento_id": procedimento_id,
            "ordem": etapa["ordem"],
            "texto": etapa["texto"],
            "foto_url": etapa.get("foto_url"),
        }
        for etapa in etapas
    ]
    response = supabase.table("etapas").insert(registros).execute()
    return response.data


def excluir_etapas(procedimento_id: int) -> None:
    supabase.table("etapas").delete().eq("procedimento_id", procedimento_id).execute()
