from supabase import create_client, Client

url: str = "https://hcoerrgtknqtrodveddf.supabase.co"
key: str = "sb_publishable_yDsK84L690CA82OeHQ3nLg_CT-06Bhm"

supabase: Client = create_client(url, key)
