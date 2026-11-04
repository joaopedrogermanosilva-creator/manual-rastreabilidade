import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).with_name(".env"))

host = "aws-0-us-east-1.pooler.supabase.com"
port = "6543"
dbname = "postgres"
user = "postgres.hcoerrgtknqtrodveddf"
password = os.getenv("SUPABASE_DB_PASSWORD")

if not password:
    raise RuntimeError("Defina SUPABASE_DB_PASSWORD no arquivo .env local.")

if os.path.exists("fase_ajuda.sql"):
    with open("fase_ajuda.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    try:
        conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password, connect_timeout=10)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql_script)
        cur.close()
        conn.close()
        print("[ok] Tabela 'configuracoes' criada no banco!")
    except Exception as e:
        print(f"[ERRO] {e}")
else:
    print("[AVISO] Arquivo fase_ajuda.sql não encontrado.")
