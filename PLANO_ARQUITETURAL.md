# Plano arquitetural — evolução do Manual de Rastreabilidade

**Data:** 1 de novembro de 2026  
**Escopo:** planejamento baseado no código local e em [AUDITORIA_SUPABASE.md](./AUDITORIA_SUPABASE.md). Não houve alterações no aplicativo, banco, Storage, GitHub ou Render.

## Arquitetura atual

### Tecnologias e fluxo

- **Backend:** Python 3.12, FastAPI e Uvicorn.
- **Interface:** HTML renderizado no servidor com Jinja2, CSS e JavaScript.
- **Persistência e arquivos:** Supabase PostgreSQL pela API Supabase/PostgREST e Supabase Storage.
- **Hospedagem/PWA:** Render; manifesto, ícones e Service Worker servidos pela aplicação.
- **Dependências principais declaradas em `requirements.txt`:** `fastapi==0.162.0`, `uvicorn==0.54.0`, `supabase==2.33.0`, `Jinja2==3.1.6` e `python-multipart==0.0.32`. O arquivo também fixa dependências transitivas. A versão declarada em `runtime.txt` é Python 3.12.0.

O fluxo normal é: navegador → rota FastAPI em `app/routes.py` → funções de dados em `app/dados.py` → cliente compartilhado em `supabase_client.py` → Supabase. As rotas montam templates Jinja e servem HTML; não há separação atual em API JSON e SPA.

### Estrutura do backend e frontend

```text
main.py                         inicializa FastAPI, arquivos estáticos, manifest e Service Worker
supabase_client.py              inicializa o cliente Supabase compartilhado
app/
  routes.py                     páginas, formulários, CRUD e upload
  dados.py                      consultas e gravações no Supabase
  templates/
    base.html                   layout, menu, tema, pesquisa e registro do Service Worker
    index.html                  página inicial e atalhos
    categoria.html              procedimentos por categoria
    busca.html                  resultados de busca
    tarefa.html                 detalhe do procedimento e ações
    form.html                   criação de procedimento
    form_editar.html            edição de procedimento
  static/
    css/style.css               identidade visual, temas e responsividade
    js/menu.js                  abre e fecha menu lateral
    js/theme.js                 alternância de tema e localStorage
    js/sw.js, sw.js             scripts do Service Worker
    manifest.json, img/         manifesto e ícones PWA
```

O runtime usa principalmente `main.py`, `supabase_client.py` e `app/`. Há também scripts auxiliares na raiz; vários escrevem arquivos diretamente e não devem ser considerados parte do runtime nem executados sem revisão.

## Funcionamento das funcionalidades existentes

### Rotas existentes

Em `app/routes.py`:

| Método | Rota | Responsabilidade |
|---|---|---|
| GET | `/` | Página inicial; carrega as categorias para o template. |
| GET | `/categoria/{slug}` | Confere o slug e lista os procedimentos dessa categoria. |
| GET | `/buscar?q=...` | Executa a pesquisa global e mostra resultados. |
| GET | `/tarefa/novo` | Mostra o formulário de criação. |
| POST | `/tarefa/novo` | Converte campos de texto em listas, tenta enviar um arquivo, grava o procedimento e redireciona à categoria. |
| GET | `/tarefa/{proc_id}/editar` | Carrega um procedimento e mostra o formulário de edição. |
| POST | `/tarefa/{proc_id}/editar` | Atualiza os campos do procedimento e tenta enviar um arquivo. |
| POST | `/tarefa/{proc_id}/excluir` | Exclui o procedimento e redireciona à categoria. |
| GET | `/tarefa/{proc_id}` | Mostra os detalhes do procedimento. |

Em `main.py`:

| Método | Rota | Responsabilidade |
|---|---|---|
| GET | `/sw.js` | Serve o Service Worker a partir da raiz, com escopo do PWA. |
| GET | `/manifest.json` | Serve o manifesto do PWA. |
| GET | `/static/...` | Arquivos estáticos montados pelo FastAPI. |

Não há modelos Pydantic próprios para os registros; as operações passam dicionários à biblioteca Supabase.

### CRUD e categorias

`app/dados.py` consulta `categorias` e `procedimentos`. A aplicação usa `categorias.slug`, `titulo` e `descricao`; procedimentos usam `id`, `categoria_slug`, `titulo`, `resumo`, `objetivo`, `como_realizar`, `pontos_atencao` e `arquivo_url`.

O CRUD associa procedimentos à categoria pelo valor `categoria_slug`. A auditoria automática retornou **4 linhas visíveis em `categorias` e 6 em `procedimentos`** para a credencial/role consultada; encontrou zero slugs sem correspondência e zero `categoria_slug` nulo entre os registros visíveis. Isso não prova o total irrestrito nem o schema completo. Tipos, chaves e constraints reais continuam não confirmados em [AUDITORIA_SUPABASE.md](./AUDITORIA_SUPABASE.md).

As categorias do menu lateral são carregadas dinamicamente por `get_categorias()`. A página inicial, em `index.html`, não usa essa coleção para os atalhos: contém links fixos para `operacoes`, `documentos`, `escala` e `rastreio`. A auditoria confirmou quatro categorias visíveis, mas não confirmou que esses quatro slugs sejam exatamente os slugs atuais no banco.

### Upload e apresentação de arquivos

Os formulários `form.html` e `form_editar.html` enviam `multipart/form-data` e aceitam `.pdf,image/*` no seletor do navegador. As rotas recebem `UploadFile`, leem o conteúdo e tentam enviá-lo ao bucket `documentos`, gerando URL pública. A auditoria não confirmou a existência ou as políticas atuais desse bucket.

`tarefa.html` identifica PDF pela terminação `.pdf`; outros arquivos são exibidos como imagem. A substituição de anexo na edição tem um problema conhecido: embora a rota calcule uma URL, `atualizar_procedimento()` não inclui `arquivo_url` no payload de update. Além disso, falhas de upload são capturadas e impressas, mas o fluxo continua e pode redirecionar sem o arquivo. Não há validação de MIME/tamanho no servidor nem remoção coordenada de objetos do Storage na exclusão.

Para fotos individuais por etapa, o campo único `arquivo_url` não é suficiente. O planejamento deve manter compatibilidade com anexos legados e introduzir relações próprias para etapas e respectivos arquivos.

### Templates, navegação e pesquisa

`base.html` é o layout compartilhado. O menu lateral lista as categorias recebidas pelo servidor; o cabeçalho inclui acesso à busca e alternância de tema. O menu móvel usa overlay e `menu.js`. `theme.js` guarda o tema em `localStorage`; o CSS fornece tema claro/escuro e regras para telas de até 600 px.

`categoria.html` lista cards de procedimentos. `tarefa.html` apresenta objetivo, passos, pontos de atenção, anexo e ações de editar/excluir. Os formulários coletam passos e pontos de atenção como texto com uma entrada por linha.

A pesquisa global usa GET em `/buscar?q=...`; `buscar_procedimentos()` aplica `ilike` a título, resumo e objetivo. Não consulta atualmente os passos, pontos de atenção, documentos ou arquivos. Não tem escopo de pasta, busca de descendentes, paginação nem limite explícito configurado pela aplicação.

O Service Worker atual não implementa cache offline; seu handler `fetch` deixa as requisições seguirem o comportamento normal do navegador. O PWA instalado deve ser preservado, mas não se deve assumir consulta offline funcional.

## Problemas encontrados

1. **Schema real incompleto:** a API REST não permitiu descobrir tipos, chaves, índices, constraints ou policies; esses detalhes precisam ser validados antes da migration.
2. **Autenticação e papéis ausentes no código:** rotas de escrita não exigem login nem autorização. As policies do Supabase não foram confirmadas.
3. **Categorias parcialmente dinâmicas:** o menu é dinâmico, mas os atalhos da home são fixos.
4. **Compatibilidade ligada ao slug:** listas, redirects e breadcrumbs dependem de `categoria_slug`; removê-lo ou renomeá-lo quebraria links e fluxo atual.
5. **Upload sem confiabilidade suficiente:** exceções não impedem o falso sucesso, a edição não persiste a nova URL, a validação é apenas no navegador e a identificação de PDF é baseada em sufixo.
6. **Busca incompleta para o novo escopo:** a consulta atual cobre apenas três campos de procedimento e não inclui conteúdo de pasta, documento ou etapas.
7. **Escopo de permissão de editor ainda precisa ser formalizado:** “conforme autorização” pode significar acesso global de edição ou autorização por pasta. Isso afeta schema, UI, endpoints e policies.
8. **Risco de estado compartilhado na autenticação:** o cliente Supabase é singleton. Não se deve trocar token/sessão mutável desse cliente global por requisição em uma aplicação concorrente; autenticação precisa usar cliente/request context apropriado.
9. **UX de edição a verificar:** `form_editar.html` contém expressões Jinja `join` cujo separador aparece quebrado em linhas no arquivo. Isso pode impedir o parsing do template; confirmar por teste de renderização antes de ampliar o formulário.
10. **Codificação de dependências:** a auditoria anterior observou `requirements.txt` em UTF-16 LE. Como o Render usa `pip install -r requirements.txt`, validar a instalação em ambiente local/staging; não alterar isso nesta etapa.

## Arquitetura futura recomendada

Princípio central: **evolução aditiva e incremental**. Manter FastAPI, Jinja2, HTML/CSS/JavaScript, Supabase, Render e os ativos PWA. Não substituir o CRUD nem recriar a interface.

### Entidades e relações

Schema a fechar somente depois de reconciliar com as informações reais do Supabase:

- **`pastas`**: `id UUID`, `parent_id UUID NULL` autorreferente, `nome`, `descricao`, `icone`, `ordem` e timestamps. Índice em `parent_id`; impedir auto-parentesco e ciclos. Não usar limite artificial de profundidade. Exclusão em RESTRICT e só permitir pastas vazias.
- **`procedimentos`**: preservar IDs e todos os campos atuais; adicionar `folder_id UUID NULL` inicialmente, com FK para `pastas.id` e exclusão RESTRICT. Manter `categoria_slug` durante toda a transição.
- **Mapeamento legado categoria→pasta**: representar o slug antigo na pasta ou em tabela de mapeamento. Só criar FK para `categorias` depois de confirmar PK/UNIQUE real de `slug`; sem isso, não presumir integridade que talvez não exista.
- **`documentos`** (tabela de metadados): UUID, `folder_id`, nome, descrição, caminho do objeto no Storage, nome original, MIME type e timestamps. Tabela no banco é distinta do bucket Storage também chamado `documentos`; considerar nome como `arquivos` se isso evitar ambiguidade.
- **`procedimento_etapas`** (fase futura): FK para procedimento, posição/ordem, conteúdo textual e metadados. Arquivos de etapas em tabela relacionada a etapas, com Storage path, para permitir múltiplas fotos por etapa sem sobrecarregar `arquivo_url`.
- **Perfil de usuário**: relação com `auth.users.id` e papel controlado (`admin`, `editor`, `collaborator`). Para edição restrita por pasta, adicionar tabela de concessões usuário/pasta/papel em vez de inferir permissões pelo caminho do nome.

`parent_id` é o modelo de adjacência apropriado para profundidade variável. A movimentação deve executar validação transacional para impedir ciclos. Para listar breadcrumbs e buscar em uma pasta e descendentes, preferir uma consulta recursiva no PostgreSQL exposta por RPC/view cuidadosamente autorizada, em vez de várias chamadas REST por nível. RLS e contexto de usuário devem continuar aplicados nessa consulta.

Para ordenar tipos mistos (pastas, procedimentos e documentos), definir uma ordenação estável por `ordem` e desempate por tipo/ID. A operação de reordenar deve atualizar os irmãos atomicamente. Se produto exigir posição global única e forte entre tipos, considerar uma tabela comum de entradas de pasta com constraints/FKs adequadas, após validar o custo e o desenho no schema real.

### Autenticação e autorização

Supabase Auth é compatível com o stack existente e oferece identidade integrada às policies PostgreSQL. Como o frontend é renderizado no servidor, planejar login/logout e sessão no backend, com cookies `HttpOnly`, `Secure` em produção e `SameSite` apropriado; nunca armazenar token de sessão em `localStorage`. Validar JWT/sessão em cada requisição protegida, renovar tokens com segurança e invalidar sessão no logout. Forms que usam sessão cookie precisam de proteção CSRF.

Usar dependências/helpers FastAPI para carregar usuário e papel, e aplicar autorização em rotas e operações de dados. Não confiar apenas em esconder botões. RLS deve reforçar as permissões no banco. Preferir cliente Supabase por requisição com token do usuário ou estratégia equivalente; não mutar sessão do singleton compartilhado entre requisições.

Semântica proposta:

- **Administrador:** gestão de usuários/papéis, pastas e todos os conteúdos.
- **Editor:** criar/editar/mover conteúdo apenas no escopo autorizado; permitir exclusão de conteúdo somente se isso for decidido explicitamente.
- **Colaborador:** leitura e pesquisa dos conteúdos autorizados.

A exclusão de pasta permanece somente para pastas vazias, confirmada pelo servidor. Ainda é necessário aprovar se editor terá permissão por pasta ou global e se editor poderá excluir procedimentos/documentos.

### Rotas futuras, mantendo as atuais

Adicionar rotas hierárquicas e administrativas sem remover rotas existentes:

- página de pasta por ID estável, com breadcrumb, subpastas, conteúdo, contagens e pesquisa com escopo;
- operações administrativas POST para criar/renomear/mover/reordenar pasta;
- criar/editar/mover procedimentos e documentos com `folder_id`;
- exclusão de pasta que falha de forma explícita se existir subpasta, procedimento ou documento associado;
- autenticação/login/logout e fluxo de recuperação, se habilitado.

Preservar `/`, `/buscar?q=...`, `/tarefa/{proc_id}` e as rotas POST atuais durante a migração. `/categoria/{slug}` deve resolver o slug legado para a pasta correspondente e renderizar a listagem nova ou redirecionar de modo compatível. Não mudar a URL de produção.

## Estratégia de migração

1. **Confirmar o schema real e policies:** usar uma conexão PostgreSQL de leitura mínima ou outro método autorizado. Registrar PKs, FKs, tipos, RLS, Storage e constraints antes de escrever DDL.
2. **Inventariar dados:** contagens não filtradas sob autorização adequada, slugs, duplicatas, `NULL`, órfãos e registros com anexos. Comparar totais antes/depois em cada etapa.
3. **Preparar staging e rollback:** backup restaurável de banco e inventário dos objetos Storage. Ensaiar a migração e reversão em staging.
4. **Criar tabela de pastas e pastas legadas:** gerar uma pasta para cada categoria existente, mantendo nome/descrição e mapeamento estável de slug. Não apagar nem renomear `categorias`.
5. **Adicionar `folder_id` nullable aos procedimentos:** deixar registros existentes intactos até validar mapeamento. Backfill por slug e registrar não mapeados; não impor NOT NULL nessa fase.
6. **Deploy compatível:** aplicação continua lendo `categoria_slug`; novas consultas passam a resolver a pasta com fallback legado. Preservar URLs antigas.
7. **Testar CRUD, busca e navegação:** validar também a compatibilidade das páginas instaladas/PWA e identidade visual em telas móveis.
8. **Adicionar autenticação/RLS gradualmente:** criar primeiro fluxo e conta de administrador; testar cada papel em staging. Não ativar bloqueio global sem garantir recuperação administrativa e leitura permitida aos colaboradores.
9. **Adicionar documentos e Storage:** migrar metadados/caminhos sem mover ou apagar objetos existentes; validar acesso antes de tornar bucket privado.
10. **Etapas com fotos:** implementar em fase separada, depois do modelo estável para documentos, sem converter ou perder o conteúdo atual de `como_realizar`.
11. **Desativar compatibilidade somente após evidência:** manter `categoria_slug`, rotas antigas e leitura dual até logs/testes confirmarem que clientes e links existentes não dependem mais do formato antigo. Remoção exige aprovação posterior, migration própria e rollback.

## Etapas de implementação

1. **Descoberta de schema e requisitos finais:** confirmar constraints e definir escopo de editores, política de exclusão de conteúdo, visibilidade de documentos e bootstrap do admin.
2. **Modelo de dados e migration aditiva:** pastas, associação opcional e índices/FKs confirmados; sem remover tabelas/campos atuais.
3. **Camada de dados compatível:** funções de consulta hierárquica e mapeamento legado isoladas em `app/dados.py` ou módulo dedicado, mantendo chamadas atuais.
4. **Leitura de pastas:** página de pasta, subpastas, breadcrumb, retorno, contagens e busca por descendentes.
5. **Associar CRUD existente:** formularios preservam campos e dados; criar/editar conteúdo seleciona pasta e aceita vínculo legado durante transição.
6. **Administração:** criar, renomear, mover, ordenar e excluir somente pasta vazia, com checagens atômicas e mensagens claras.
7. **Login e papéis:** login/logout, sessão segura, verificações FastAPI e policies Supabase/RLS alinhadas.
8. **Documentos:** entidade de metadados, upload validado, Storage, recuperação e autorização.
9. **Etapas e fotos:** tabela de etapas e anexos por etapa.
10. **Ajustes de UX e PWA:** manter tema, menu, ícones, manifesto e URL; adicionar cache offline só se for requisito aprovado.
11. **Staging e produção:** regressão completa, backup e plano de rollback antes de deploy; deploy só com autorização.

## Testes necessários

### Regressão atual

- Home, menu dinâmico, atalhos, tema escuro/claro e links de categorias.
- Consulta de procedimento e campos existentes, incluindo listas de passos/pontos.
- Criar, editar e excluir procedimento com e sem arquivo.
- Pesquisa global antiga em `/buscar?q=...`.
- `/categoria/{slug}` e `/tarefa/{proc_id}` com URLs já usadas.
- Registro e escopo raiz do Service Worker, manifesto, ícones e instalação PWA.

### Hierarquia e integridade

- Raiz, vários níveis, pasta vazia e pastas com conteúdo.
- Breadcrumb e voltar em cada profundidade.
- Mover pasta para outro ramo; rejeitar mover para si ou para descendente.
- Reordenar tipos mistos e manter ordem estável em concorrência.
- Excluir pasta vazia; bloquear pasta com subpastas, procedimentos ou documentos.
- Pesquisa global e pesquisa por pasta que inclui todos os descendentes, sem duplicatas.
- IDs, FKs, slugs legados e contagens preservados antes/depois do backfill.

### Autorização e sessão

- Sem sessão: negar rotas protegidas e manter apenas páginas explicitamente públicas, se houver.
- Colaborador: leitura e busca autorizadas; rejeitar toda tentativa de escrita.
- Editor: criar/editar apenas dentro do escopo permitido; rejeitar pastas fora do escopo.
- Administrador: operação total conforme política aprovada.
- Token expirado, logout, renovação, CSRF, acesso direto a URL e tentativa de alterar ID no formulário.
- RLS testado com papel de usuário normal, sem service role no fluxo de aplicação.

### Upload, interface e deploy

- Extensão, MIME real, tamanho, nome, colisão, falha de rede e feedback visível.
- PDF e imagem em conteúdo e documento; acesso autorizado; substituição e exclusão sem órfãos.
- Renderização do template de edição e listas legadas; teste em viewport móvel, teclado e leitor de tela.
- Instalação/deploy de staging e logs do Render; conferir que dependências fixadas podem ser instaladas.
- Testes em navegador para links, formulário, sessão, breadcrumbs, pesquisa e PWA antes de produção.

## Riscos e medidas preventivas

| Risco | Medida preventiva |
|---|---|
| Schema real divergir das hipóteses do código | Confirmar metadados e constraints antes da migration; não copiar schema presumido. |
| Perda ou duplicação de procedimentos no backfill | `folder_id` inicialmente nullable, backup, relatório de slugs órfãos e comparação de totais. |
| Quebra de links antigos | Preservar slugs e rotas; mapear slug legado para pasta; teste com URLs conhecidas. |
| Ciclo ou órfão na hierarquia | Transação/RPC, FK RESTRICT, validação recursiva e testes de concorrência. |
| Consulta recursiva lenta ou sem RLS | RPC recursiva com índices em `parent_id`, filtros e autorização de usuário; validar plano e volume em staging. |
| Editor ultrapassar seu escopo | Autorização em cada operação, checando origem e destino, reforçada por RLS. |
| Bloqueio de acesso administrativo | Criar e testar administrador inicial, recuperação de senha e sessão antes de exigir login geral. |
| Mudança de Storage invalidar URLs legadas | Preservar objetos/caminhos e testar autorização; migração de URLs separada e reversível. |
| PWA manter arquivos antigos em cache | Service Worker atual não faz cache; verificar clientes instalados e planejar atualização de assets/versões sem remover o registro na raiz. |
| Regressão visual ou móvel | Reutilizar tokens/classes atuais do CSS e validar telas pequenas e temas. |
| Deploy interrompido por dependências/configuração | Validar instalação e inicialização em staging; conferir `requirements.txt`/`runtime.txt` antes de publicar. |

**Estado final desta etapa:** somente este documento de planejamento deve ser novo. Nenhuma recomendação foi implementada; autenticação, schema e migração continuam sujeitos à aprovação.
