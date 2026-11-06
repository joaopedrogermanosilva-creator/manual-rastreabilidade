import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
password = os.getenv("SUPABASE_DB_PASSWORD")

if not password:
    print("❌ Senha do banco não encontrada no .env. Verifique se o arquivo .env tem a variável SUPABASE_DB_PASSWORD.")
    exit()

host = "aws-0-us-east-1.pooler.supabase.com"
port = "6543"
dbname = "postgres"
user = "postgres.hcoerrgtknqtrodveddf"

sql_file = Path("fase_busca_fuzzy.sql")
if not sql_file.exists():
    print("❌ Arquivo fase_busca_fuzzy.sql não encontrado.")
    exit()

with open(sql_file, "r", encoding="utf-8") as f:
    sql_script = f.read()

try:
    print("Conectando ao banco de dados...")
    conn = psycopg2.connect(
        host=host, port=port, dbname=dbname, user=user, password=password, connect_timeout=10
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql_script)
    cur.close()
    conn.close()
    print("\n[ok] Busca Inteligente ativada no banco de dados!")
    print("Agora o app vai achar os procedimentos mesmo se você digitar com erros.")
except Exception as e:
    print(f"\n[ERRO] Falha ao ativar a busca: {e}")
