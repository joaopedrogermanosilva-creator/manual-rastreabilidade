import os

# Instala a biblioteca que cria arquivos do Word
os.system("pip install python-docx -q")

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Título principal
titulo = doc.add_heading('Resumo do Projeto: Manual de Rastreabilidade', 0)
titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Visão Geral
doc.add_heading('1. Visão Geral', level=1)
doc.add_paragraph('Sistema web responsivo (PWA) para consulta de procedimentos operacionais de recebimento. O app roda em Python/FastAPI, usa Supabase para banco de dados e armazenamento de arquivos, e está hospedado no Render.')

# Tecnologias
doc.add_heading('2. Tecnologias Utilizadas', level=1)
doc.add_paragraph('• Backend: Python, FastAPI, Uvicorn', style='List Bullet')
doc.add_paragraph('• Frontend: HTML, CSS, JavaScript, Jinja2', style='List Bullet')
doc.add_paragraph('• Banco de Dados: Supabase (PostgreSQL)', style='List Bullet')
doc.add_paragraph('• Armazenamento: Supabase Storage (Bucket: documentos)', style='List Bullet')
doc.add_paragraph('• Hospedagem: Render (plano gratuito)', style='List Bullet')
doc.add_paragraph('• Versionamento: Git / GitHub (joaopedrogermanosilva-creator/manual-rastreabilidade)', style='List Bullet')

# O que funciona
doc.add_heading('3. O que já está 100% Funcionando', level=1)
doc.add_paragraph('• Tela inicial com busca global e menu lateral (hambúrguer).', style='List Bullet')
doc.add_paragraph('• CRUD completo (criar, ler, editar, excluir) de procedimentos conectado ao Supabase.', style='List Bullet')
doc.add_paragraph('• Design responsivo (tema claro/escuro) com ícones Phosphor.', style='List Bullet')
doc.add_paragraph('• PWA configurado (instalável no celular como app nativo).', style='List Bullet')
doc.add_paragraph('• Conexão segura com o Supabase via variáveis de ambiente no Render.', style='List Bullet')

# O Problema
doc.add_heading('4. O PROBLEMA ATUAL (O que precisa ser resolvido)', level=1)
p = doc.add_paragraph()
p.add_run('O upload de imagens/PDFs não está funcionando na nuvem (Render). O código envia o arquivo, mas a imagem não aparece na tela e não salva no bucket.').bold = True

doc.add_heading('O que já foi tentado:', level=2)
doc.add_paragraph('1. O bucket "documentos" foi criado com sucesso via API REST (usando a chave sb_secret_).', style='List Number')
doc.add_paragraph('2. A variável de ambiente SUPABASE_KEY no painel do Render foi atualizada para a chave secreta.', style='List Number')

doc.add_heading('Código do supabase_client.py:', level=2)
p = doc.add_paragraph('import os\nfrom supabase import create_client, Client\nurl = "https://hcoerrgtknqtrodveddf.supabase.co"\nkey = os.getenv("SUPABASE_KEY", "chave_publica_fallback")\nsupabase = create_client(url, key)')
p.style.font.name = 'Courier New'
p.style.font.size = Pt(10)

doc.add_heading('Código de Upload (routes.py):', level=2)
p = doc.add_paragraph('if arquivo and arquivo.filename:\n    try:\n        path = f"proc_{titulo.replace(\' \', \'_\')}_{arquivo.filename}"\n        supabase.storage.from_("documentos").upload(path, arquivo.file.read())\n        url = supabase.storage.from_("documentos").get_public_url(path)\n    except Exception as e: \n        print(f"Erro Upload: {e}")')
p.style.font.name = 'Courier New'
p.style.font.size = Pt(10)

doc.add_heading('Suspeitas do problema:', level=2)
doc.add_paragraph('• RLS (Row Level Security): O bucket pode estar bloqueando o upload por falta de políticas.', style='List Bullet')
doc.add_paragraph('• Biblioteca do Python: A biblioteca supabase-py pode estar com bug com a chave secreta.', style='List Bullet')

# Salva o arquivo
doc.save('Resumo_Projeto_Rastreabilidade.docx')
print("[ok] Arquivo 'Resumo_Projeto_Rastreabilidade.docx' criado com sucesso na pasta do projeto!")
