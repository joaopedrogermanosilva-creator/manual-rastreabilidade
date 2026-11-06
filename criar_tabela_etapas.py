import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
password = os.getenv("SUPABASE_DB_PASSWORD")

if not password:
    print("❌ Senha do banco não encontrada no .env.")
    exit()

host = "aws-0-us-east-1.pooler.supabase.com"
port = "6543"
dbname = "postgres"
user = "postgres.hcoerrgtknqtrodveddf"

sql_file = Path("fase_etapas.sql")
if not sql_file.exists():
    print("❌ Arquivo fase_etapas.sql não encontrado.")
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
    print("\n[ok] Tabela 'etapas' criada com sucesso no banco!")
    print("Agora o app está pronto para salvar os passos com fotos.")
except Exception as e:
    print(f"\n[ERRO] {e}")
