from supabase_client import supabase

try:
    # Tenta criar o bucket "documentos" como público
    resposta = supabase.storage.create_bucket("documentos", options={"public": True})
    print("[ok] Bucket 'documentos' criado com sucesso!")
except Exception as e:
    if "already exists" in str(e).lower():
        print("[ok] O bucket 'documentos' já existe.")
    else:
        print(f"[ERRO] Não foi possível criar o bucket: {e}")
