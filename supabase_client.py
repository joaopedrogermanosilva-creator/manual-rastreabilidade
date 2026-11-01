import os
from supabase import create_client, Client

url: str = "https://hcoerrgtknqtrodveddf.supabase.co"
key: str = str(
    os.getenv(
        "SUPABASE_KEY",
        "sb_publishable_yDsK84L690CA82OeHQ3nLg_CT-06Bhm",
    )
).strip()

# A MÁGICA ESTÁ AQUI: str() garante que o Python não envie um objeto URL
supabase: Client = create_client(str(url).strip(), key)
