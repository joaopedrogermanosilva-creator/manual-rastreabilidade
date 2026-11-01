import psycopg2
import os

# Conexão direta com o banco
host = "db.hcoerrgtknqtrodveddf.supabase.co"
port = "5432"
dbname = "postgres"
user = "postgres"
password = "@Rastreabilidade"

# Lê o arquivo SQL que a IA criou
if not os.path.exists("fase1_pastas.sql"):
    print("[ERRO] O arquivo fase1_pastas.sql não foi encontrado na pasta atual.")
else:
    with open("fase1_pastas.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    try:
        print("Conectando ao banco e criando as tabelas...")
        conn = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=user, password=password, connect_timeout=10
        )
        conn.autocommit = True # Permite executar o CREATE TABLE e COMMIT
        
        cur = conn.cursor()
        cur.execute(sql_script)
        cur.close()
        conn.close()
        
        print("\n[ok] SUCESSO! As tabelas 'pastas' e 'anexos' foram criadas no banco de dados.")
        print("Agora você pode atualizar a página no navegador e a aba 'Pastas' vai funcionar!")
        
    except Exception as e:
        print(f"\n[ERRO] Falha ao criar as tabelas: {e}")
