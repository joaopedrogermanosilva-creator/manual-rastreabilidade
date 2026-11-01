codigo = """import os
from supabase import create_client, Client

url: str = "https://hcoerrgtknqtrodveddf.supabase.co"
key: str = os.getenv("SUPABASE_SECRET_KEY", "sb_publishable_yDsK84L690CA82OeHQ3nLg_CT-06Bhm")

# Força a conversão para string (texto) para evitar o erro TypeError: got 'URL'
supabase: Client = create_client(str(url), str(key))
"""
with open("supabase_client.py", "w", encoding="utf-8") as f:
    f.write(codigo)
print("[ok] supabase_client.py corrigido (conversao para string)")
