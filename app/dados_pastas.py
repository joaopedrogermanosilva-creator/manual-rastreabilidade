from uuid import UUID

from supabase_client import supabase

_UNSET = object()


def listar_pastas(parent_id: UUID | str | None = None):
    query = supabase.table("pastas").select("id,nome,descricao,parent_id,ordem")
    if parent_id is None:
        response = query.is_("parent_id", "null").execute()
    else:
        response = query.eq("parent_id", str(parent_id)).execute()
    return sorted(response.data, key=lambda folder: (folder["ordem"], folder["nome"].casefold()))


def listar_todas_pastas():
    response = (
        supabase.table("pastas")
        .select("id,nome,descricao,parent_id,ordem")
        .execute()
    )
    return sorted(response.data, key=lambda folder: (folder["ordem"], folder["nome"].casefold()))


def buscar_pasta(pasta_id: UUID | str):
    response = (
        supabase.table("pastas")
        .select("id,nome,descricao,parent_id,ordem")
        .eq("id", str(pasta_id))
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


def listar_procedimentos_da_pasta(pasta_id: UUID | str):
    response = (
        supabase.table("procedimentos")
        .select("*")
        .eq("pasta_id", str(pasta_id))
        .execute()
    )
    return response.data


def obter_breadcrumb(pasta_id: UUID | str):
    caminho = []
    visitadas = set()
    pasta = buscar_pasta(pasta_id)

    while pasta:
        pasta_atual_id = str(pasta["id"])
        if pasta_atual_id in visitadas:
            raise RuntimeError("Ciclo detectado na hierarquia de pastas.")
        visitadas.add(pasta_atual_id)
        caminho.append(pasta)
        parent_id = pasta.get("parent_id")
        pasta = buscar_pasta(parent_id) if parent_id else None

    caminho.reverse()
    return caminho


def listar_opcoes_pasta():
    pastas = listar_todas_pastas()
    por_id = {str(pasta["id"]): pasta for pasta in pastas}
    opcoes = []

    for pasta in pastas:
        partes = [pasta["nome"]]
        parent_id = pasta.get("parent_id")
        visitadas = {str(pasta["id"])}
        while parent_id:
            parent_id = str(parent_id)
            if parent_id in visitadas:
                raise RuntimeError("Ciclo detectado na hierarquia de pastas.")
            visitadas.add(parent_id)
            parent = por_id.get(parent_id)
            if parent is None:
                break
            partes.append(parent["nome"])
            parent_id = parent.get("parent_id")
        opcoes.append({**pasta, "caminho": " / ".join(reversed(partes))})

    return opcoes


def criar_pasta(nome: str, descricao: str = "", parent_id: UUID | str | None = None, ordem: int = 0):
    dados = {
        "nome": nome.strip(),
        "descricao": descricao.strip(),
        "parent_id": str(parent_id) if parent_id else None,
        "ordem": ordem,
    }
    response = supabase.table("pastas").insert(dados).execute()
    return response.data[0] if response.data else None


def atualizar_pasta(
    pasta_id: UUID | str,
    nome: str | None = None,
    descricao: str | None = None,
    parent_id=_UNSET,
    ordem: int | None = None,
):
    pasta_atual = buscar_pasta(pasta_id)
    if not pasta_atual:
        return None

    dados = {}
    if nome is not None:
        dados["nome"] = nome.strip()
    if descricao is not None:
        dados["descricao"] = descricao.strip()
    if ordem is not None:
        dados["ordem"] = ordem

    if parent_id is not _UNSET:
        if parent_id:
            parent = buscar_pasta(parent_id)
            if not parent:
                raise ValueError("A pasta superior informada não existe.")
            atual = parent
        else:
            atual = None
        visitadas = set()
        while atual:
            atual_id = str(atual["id"])
            if atual_id == str(pasta_id):
                raise ValueError("Não é possível mover uma pasta para dentro de si mesma ou de uma descendente.")
            if atual_id in visitadas:
                raise RuntimeError("Ciclo detectado na hierarquia de pastas.")
            visitadas.add(atual_id)
            parent_id_atual = atual.get("parent_id")
            atual = buscar_pasta(parent_id_atual) if parent_id_atual else None
        dados["parent_id"] = str(parent_id) if parent_id else None

    if not dados:
        return pasta_atual
    response = (
        supabase.table("pastas")
        .update(dados)
        .eq("id", str(pasta_id))
        .select("*")
        .execute()
    )
    return response.data[0] if response.data else None


def excluir_pasta(pasta_id: UUID | str):
    if listar_pastas(pasta_id):
        return False
    if listar_procedimentos_da_pasta(pasta_id):
        return False

    response = (
        supabase.table("pastas")
        .delete()
        .eq("id", str(pasta_id))
        .select("id")
        .execute()
    )
    return bool(response.data)
