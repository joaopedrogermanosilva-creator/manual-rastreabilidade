# Sobrescreve o arquivo forçando tudo a ser string pura
codigo = """import os
from supabase import create_client, Client

url: str = "https://hcoerrgtknqtrodveddf.supabase.co"
key: str = os.getenv("SUPABASE_SECRET_KEY", "sb_publishable_yDsK84L690CA82OeHQ3nLg_CT-06Bhm")

# A MÁGICA ESTÁ AQUI: str() garante que o Python não envie um objeto URL
supabase: Client = create_client(str(url).strip(), str(key).strip())
"""
with open("supabase_client.py", "w", encoding="utf-8") as f:
    f.write(codigo)
print("[ok] supabase_client.py reescrito e blindado!")
