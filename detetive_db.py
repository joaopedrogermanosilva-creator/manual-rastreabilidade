import psycopg2
import os

project_ref = "hcoerrgtknqtrodveddf"
password = "@Rastreabilidade"

# Lista de regiões e clusters que o Supabase usa
regions = ["sa-east-1", "us-east-1", "us-west-1", "eu-central-1", "ap-southeast-1"]
clusters = ["aws-0", "aws-1", "aws-2"]

hosts = []
for cluster in clusters:
    for region in regions:
        hosts.append(f"{cluster}-{region}.pooler.supabase.com")

# Adiciona a conexão direta também
hosts.append(f"db.{project_ref}.supabase.co")

# Lê o SQL
if os.path.exists("fase1_pastas.sql"):
    with open("fase1_pastas.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
else:
    print("[ERRO] O arquivo fase1_pastas.sql nao foi encontrado.")
    exit()

print("Iniciando busca pelo servidor correto...\n")
connected = False

for host in hosts:
    try:
        # Se for a conexão direta, usa a porta 5432 e o usuário 'postgres'
        if "db." in host:
            port = "5432"
            user = "postgres"
        else:
            port = "6543"
            user = f"postgres.{project_ref}"

        conn = psycopg2.connect(
            host=host, port=port, dbname="postgres",
            user=user, password=password, connect_timeout=3
        )
        
        print(f"[SUCESSO] Achei o servidor certo: {host}!")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql_script)
        cur.close()
        conn.close()
        print("[OK] Tabelas criadas com sucesso no banco de dados!")
        connected = True
        break # Para de procurar se achar
        
    except Exception as e:
        # Se não for o servidor certo ou a senha estiver errada, tenta o próximo
        pass

if not connected:
    print("\n[ERRO] Nao consegui conectar a nenhum servidor. A rede (mesmo no Hotspot) esta bloqueando as portas 5432/6543.")
    print("Nesse caso, a UNICA saida e rodar o SQL pelo painel do Supabase (SQL Editor).")
else:
    print("\nAgora va no navegador e de Ctrl+F5 na pagina de Pastas!")
