from datetime import datetime, timezone

from supabase_client import supabase


def get_configuracao(chave: str) -> str | None:
    response = (
        supabase.table("configuracoes")
        .select("valor")
        .eq("chave", chave)
        .limit(1)
        .execute()
    )
    return response.data[0]["valor"] if response.data else None


def salvar_configuracao(chave: str, valor: str) -> None:
    supabase.table("configuracoes").upsert(
        {
            "chave": chave,
            "valor": valor,
            "atualizado_em": datetime.now(timezone.utc).isoformat(),
        }
    ).execute()
