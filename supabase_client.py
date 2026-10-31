import os
from supabase import create_client, Client

url: str = "https://hcoerrgtknqtrodveddf.supabase.co"
# Pega a chave das variáveis de ambiente (Render). Se não achar, usa a pública como fallback.
key: str = os.getenv("SUPABASE_KEY", "sb_publishable_yDsK84L690CA82OeHQ3nLg_CT-06Bhm")

supabase: Client = create_client(url, key)
