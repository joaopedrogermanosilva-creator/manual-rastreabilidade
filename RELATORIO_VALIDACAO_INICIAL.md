# Relatório de validação inicial

**Data:** 1 de novembro de 2026  
**Escopo:** validação local somente de leitura antes da implementação. Nenhum dado foi gravado no Supabase; nenhuma migration, instalação, alteração do aplicativo, commit ou deploy foi executado.

## Resumo executivo

O ambiente virtual local está funcional para a aplicação existente: Python 3.14.5 importa FastAPI e dependências centrais; Uvicorn iniciou localmente; os templates Jinja foram compilados, incluindo `form_editar.html`; e os endpoints sem acesso ao banco usados no smoke test responderam HTTP 200.

O `requirements.txt` tem BOM UTF-16 LE, mas o parser nativo do pip interpretou corretamente 82 entradas. As 82 dependências ativas estão instaladas e satisfazem as versões declaradas no venv atual. O Render declara Python 3.12.0, enquanto o ambiente local selecionado é Python 3.14.5; portanto, esta validação não certifica o runtime de produção.

Os metadados administrativos completos do Supabase continuam indisponíveis. A auditoria anterior documentada em [AUDITORIA_SUPABASE.md](./AUDITORIA_SUPABASE.md) conseguiu apenas consultas REST limitadas; RLS, policies, schema PostgreSQL completo e configuração do bucket ainda não estão confirmados. Não se deve iniciar a migration hierárquica até obter um método de leitura autorizado para validar esses elementos.

## Testes realizados

### 1. Ambiente Python e dependências

| Teste | Resultado |
|---|---|
| Python do venv | **OK** — `.venv\Scripts\python.exe`, Python 3.14.5. |
| Import de FastAPI, Uvicorn, Jinja2, Supabase e multipart | **OK**. |
| BOM/codificação do `requirements.txt` | **Confirmado** — BOM `FF FE`, UTF-16 LE. |
| Parse do arquivo pelo parser nativo do pip | **OK** — 82 entradas interpretadas, nenhum erro. |
| Requisitos comparados com o venv | **OK** — 82 requisitos ativos verificados; zero ausentes e zero incompatibilidades de versão. |
| Instalação de pacotes | **Não realizada**. |

O venv local não corresponde à versão declarada no deploy: [runtime.txt](./runtime.txt) indica Python 3.12.0, enquanto o Python selecionado pelo VS Code e usado nos testes foi 3.14.5. A validação em Python 3.12 ainda precisa ser feita antes de certificar compatibilidade de produção.

### 2. Inicialização FastAPI/Uvicorn

O processo local `uvicorn main:app --host 127.0.0.1` iniciou e foi encerrado ao fim do teste. O endpoint OpenAPI confirmou as rotas registradas. Também foi feito smoke test via cliente HTTP local:

| GET local | Resultado |
|---|---|
| `/openapi.json` | HTTP 200 |
| `/manifest.json` | HTTP 200 |
| `/sw.js` | HTTP 200 |
| `/static/css/style.css` | HTTP 200 |
| `/static/img/icon-192.png` | HTTP 200 |
| `/static/js/menu.js` | HTTP 200 |

Esses testes não chamaram endpoints que leem ou gravam dados operacionais.

### 3. Templates Jinja2

Todos os sete templates foram compilados pelo Jinja2 sem erro: `base.html`, `busca.html`, `categoria.html`, `form.html`, `form_editar.html`, `index.html` e `tarefa.html`.

`form_editar.html` também foi renderizado com contexto sintético representativo e produziu HTML com sucesso. A hipótese anterior de erro de sintaxe nas expressões `join` não se confirmou neste teste. A renderização não valida dados reais nem o comportamento completo do formulário no navegador.

### 4. Rotas e segurança de testes sem escrita

O schema OpenAPI local registra:

| Método | Rota |
|---|---|
| GET | `/` |
| GET | `/categoria/{slug}` |
| GET | `/buscar` |
| GET | `/tarefa/novo` |
| POST | `/tarefa/novo` |
| GET | `/tarefa/{proc_id}/editar` |
| POST | `/tarefa/{proc_id}/editar` |
| POST | `/tarefa/{proc_id}/excluir` |
| GET | `/tarefa/{proc_id}` |
| GET | `/sw.js` |
| GET | `/manifest.json` |
| GET | `/static/...` |

**Podem ser testadas localmente sem consultar o banco:** `/openapi.json`, `/manifest.json`, `/sw.js` e `/static/...`; a compilação/renderização Jinja com dados sintéticos também é independente do Supabase.

**São somente GET, mas consultam o Supabase:** `/`, `/categoria/{slug}`, `/buscar` (a busca com termo consulta procedimentos), `/tarefa/novo`, `/tarefa/{proc_id}/editar` e `/tarefa/{proc_id}`. Uma chamada GET não deveria gravar dados pelo código atual, mas pode expor conteúdo e depende das permissões atuais; por isso não foram chamadas nesta validação.

**Não devem ser invocadas como smoke test:** os três POST do CRUD (`/tarefa/novo`, `/tarefa/{proc_id}/editar`, `/tarefa/{proc_id}/excluir`), pois podem gravar/excluir dados ou objetos.

### 5. PWA e assets

- `manifest.json` foi analisado como JSON válido; define `start_url: "/"` e quatro entradas de ícone.
- Os arquivos `icon-192.png` e `icon-512.png` existem e correspondem aos caminhos do manifesto.
- `base.html` referencia `/manifest.json`, `/sw.js`, CSS, `theme.js` e `menu.js`.
- O Service Worker servido na raiz existe; o handler `fetch` atual não implementa cache offline.
- Os endpoints de manifesto, Service Worker e ícones testados responderam HTTP 200.

## Acesso ao Supabase e metadados

Esta validação não realizou operações de escrita nem repetiu chamadas externas. O resultado de leitura disponível é o registrado na [AUDITORIA_SUPABASE.md](./AUDITORIA_SUPABASE.md):

- A API REST permitiu contagens de 4 categorias e 6 procedimentos visíveis à credencial usada naquela execução.
- Os registros visíveis não apresentaram slugs de categoria sem correspondência nem `categoria_slug` nulo.
- A descoberta OpenAPI respondeu HTTP 401; as tentativas em `information_schema` e `pg_catalog`, HTTP 406.
- O bucket `documentos` não foi confirmado pela listagem; a consulta direta registrada respondeu HTTP 400.
- Esses erros não provam inexistência de tabelas/policies/bucket e não revelam se RLS está habilitado.
- Nesta sessão de validação, `SUPABASE_KEY` e variáveis de conexão direta PostgreSQL não estavam definidas no ambiente local. Nenhum valor de credencial foi exibido.

**Método autorizado necessário para confirmar o restante:** conexão PostgreSQL de somente leitura já aprovada pelo administrador, com privilégios mínimos para consultar metadados e executar `SELECT` nas tabelas necessárias, sem `BYPASSRLS` e sem permissões de escrita. Para policies e configurações administrativas, a role precisa ter autorização explícita de leitura desses catálogos. Não usar `service_role`, não contornar RLS e não compartilhar credenciais em chat.

Sem esse acesso aprovado, seguem pendentes:

- schema completo e todas as tabelas;
- tipos, defaults, nulabilidade, PK/FK, constraints, índices e triggers;
- estado habilitado/forçado de RLS e policies;
- existência, visibilidade, limites e MIME types do bucket `documentos` e suas policies.

## Problemas e limitações encontrados

1. **Diferença de Python:** venv local em 3.14.5; deploy declara 3.12.0. Compatibilidade específica com 3.12 não foi testada.
2. **Metadados Supabase pendentes:** falta método autorizado de leitura dos catálogos e de configuração/policies do Storage. É o principal bloqueio para projetar e executar uma migration segura.
3. **Rotas de leitura dependem do Supabase:** não foram chamadas para evitar consultas a dados de produção durante o smoke test; o sucesso local do servidor não certifica acesso às páginas com dados.
4. **Autenticação/autorização não implementada:** o código existente não valida usuário ou papéis nas rotas do CRUD. Isso deve ser resolvido e testado antes de abrir administração de pastas.
5. **Upload ainda tem riscos conhecidos:** validação server-side de arquivo ausente, exceções de upload não impedem redirecionamento de sucesso e atualização não persiste `arquivo_url` na função de dados.
6. **Dependência auxiliar `PIL`:** análise de imports do Pylance apontou `PIL` não resolvido na ferramenta auxiliar de ícones; não é importado pelo runtime FastAPI e não afetou os testes da aplicação. Não foi instalada biblioteca.
7. **PWA sem suporte offline:** o Service Worker é pass-through e não armazena páginas/dados em cache; a instalação PWA está referenciada e os assets responderam, mas navegação offline não foi validada nem é implementada pelo handler atual.

## O que está funcionando nesta validação

- Venv local e imports centrais da aplicação.
- Interpretação de `requirements.txt` pelo parser do pip apesar de UTF-16 LE.
- Versões instaladas do venv compatíveis com as 82 entradas declaradas.
- Import e inicialização de FastAPI/Uvicorn local.
- Registro de rotas no OpenAPI local.
- Sintaxe e renderização isolada dos templates, inclusive `form_editar.html`.
- Serviço local de manifest, Service Worker, CSS, JS e ícone testados.
- Nenhum endpoint POST, migration ou operação de escrita foi executado.

## O que ainda impede a implementação segura

- Não há confirmação do schema real, constraints, RLS ou policies necessárias para desenhar as migrations e os papéis.
- Não há comprovação das políticas e visibilidade do Storage para documentos.
- O ambiente Python de produção (3.12.0) não foi validado localmente.
- A implementação de autenticação e os limites de autorização do papel editor precisam ser definidos/testados antes de proteger CRUD e pastas.

## Próxima ação técnica recomendada

1. Obter, por processo aprovado e sem compartilhar segredos, um método de consulta PostgreSQL somente leitura com privilégio mínimo; usá-lo para confirmar schema, constraints, RLS e policies. Se esse acesso não puder ser concedido, documentar o limite e não inferir a estrutura.
2. Repetir validações Python em ambiente 3.12 compatível com o Render, sem instalar ou alterar dependências em produção.
3. Em staging, testar leituras e CRUD com cópia de dados, autenticação e RLS antes de elaborar/aplicar qualquer migration.
4. Somente após aprovação do schema e dos testes, preparar migration aditiva com backup e rollback; não remover `categoria_slug`, rotas antigas nem anexos legados na primeira etapa.

## Integridade do projeto

O estado Git antes dos testes tinha os relatórios `AUDITORIA_SUPABASE.md` e `PLANO_ARQUITETURAL.md`, além de `Resumo_Projeto_Rastreabilidade.docx` e `gerar_word.py`, todos não rastreados. Não havia diferenças staged ou unstaged em arquivos rastreados. Os testes foram executados com bytecode desabilitado, não instalaram bibliotecas e não invocaram rotas de escrita.

Este relatório é o único arquivo criado nesta etapa. Não houve commit, push, deploy, migration, alteração de banco/Storage ou edição dos arquivos do aplicativo.
