import psycopg2
import os

# Tenta o Pooler na porta 6543 (IPv4) com o cluster aws-1
host = "aws-1-sa-east-1.pooler.supabase.com"
port = "6543"
dbname = "postgres"
user = "postgres.hcoerrgtknqtrodveddf"  # O nome de usuário precisa do project ref
password = "@Rastreabilidade"

# Lê o arquivo SQL
if not os.path.exists("fase1_pastas.sql"):
    print("[ERRO] O arquivo fase1_pastas.sql não foi encontrado.")
else:
    with open("fase1_pastas.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    try:
        print("Conectando ao banco via Pooler (aws-1, porta 6543)...")
        conn = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=user, password=password, connect_timeout=10
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql_script)
        cur.close()
        conn.close()
        print("\n[ok] SUCESSO! As tabelas foram criadas.")
    except Exception as e:
        print(f"\n[ERRO] {e}")
