from supabase_client import supabase

# Vamos usar a API para fazer um "alter table" direto.
# Se a sua chave publicável não tiver permissão de DDL, vamos usar a chave secreta apenas neste script.
# COLOQUE AQUI A SUA CHAVE SECRET_ QUE VOCÊ PEGOU NO PAINEL (aquela sb_secret_...)
url = "https://hcoerrgtknqtrodveddf.supabase.co"
secret_key = "COLE_AQUI_SUA_CHAVE_SECRET_QUE_VOCE_NAO_DEVE_COMPARTILHAR"

from supabase import create_client
admin_client = create_client(url, secret_key)

sql = """
ALTER TABLE procedimentos ADD COLUMN IF NOT EXISTS arquivo_url TEXT;
"""

try:
    # O Supabase não permite rodar SQL puro pela chave, mas podemos usar a API de RPC se a função existir.
    # Como não temos, vamos tentar um "hack" via HTTP (PostgREST não faz DDL).
    # A única forma de DDL pela chave de serviço é via função SQL.
    print("ATENÇÃO: Não dá para rodar DDL direto pelo supabase-py.")
    print("Vá no SQL Editor do Supabase e rode APENAS isto:")
    print(sql)
except Exception as e:
    print("Erro:", e)
