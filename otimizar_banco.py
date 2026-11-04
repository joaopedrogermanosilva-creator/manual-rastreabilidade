import os

import psycopg2
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

sql = """
-- Índice para buscar procedimentos por pasta rapidamente
CREATE INDEX IF NOT EXISTS idx_procedimentos_pasta_id ON public.procedimentos(pasta_id);

-- Índice para buscar pastas por pasta pai
CREATE INDEX IF NOT EXISTS idx_pastas_parent_id ON public.pastas(parent_id);

-- Índice para a pesquisa de texto (título, resumo)
CREATE INDEX IF NOT EXISTS idx_procedimentos_titulo ON public.procedimentos(titulo);

-- Índice para os anexos por procedimento
CREATE INDEX IF NOT EXISTS idx_anexos_procedimento_id ON public.anexos(procedimento_id);
"""

try:
    conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password, connect_timeout=10)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.close()
    print("[ok] Índices criados! O banco agora está otimizado para velocidade!")
except Exception as e:
    print(f"[ERRO] {e}")
