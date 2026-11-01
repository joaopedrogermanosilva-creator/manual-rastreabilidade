# Auditoria automática do Supabase

**Data:** 1 de novembro de 2026  
**Escopo:** auditoria somente de leitura do código local e das informações acessíveis pela API Supabase a partir do terminal local.

## Resumo executivo

A aplicação usa as tabelas `categorias` e `procedimentos` pela API REST do Supabase e usa o Storage pelo bucket esperado `documentos`. Nesta sessão, a API permitiu contar 4 categorias e 6 procedimentos visíveis à credencial atual; os slugs de categoria dos procedimentos visíveis corresponderam às categorias consultadas.

Não foi possível confirmar o schema PostgreSQL completo, chaves, constraints, índices, RLS ou políticas. O terminal não tinha uma chave Supabase definida em ambiente nem uma URL/credencial de conexão PostgreSQL direta. A API REST recusou a descoberta OpenAPI (HTTP 401) e as tentativas de acesso aos schemas `information_schema` e `pg_catalog` (HTTP 406). O bucket `documentos` não apareceu na listagem; a consulta direta ao bucket respondeu HTTP 400. Esses resultados **não provam** que o bucket não exista nem que o RLS esteja desabilitado.

## 1. Conexão e credenciais

- [supabase_client.py](./supabase_client.py) cria o cliente Supabase com uma URL fixa e consulta a variável de ambiente `SUPABASE_KEY`.
- Se `SUPABASE_KEY` não estiver definida, o código usa uma chave publishable de fallback presente no próprio arquivo. O valor não é reproduzido neste relatório.
- Neste terminal, `SUPABASE_KEY` não estava definida. O script reutilizou a configuração já existente no módulo, sem imprimir a chave.
- Não havia variáveis de conexão direta PostgreSQL disponíveis entre `DATABASE_URL`, `SUPABASE_DB_URL`, `POSTGRES_URL`, `PGHOST`, `PGDATABASE` e `PGUSER`.
- O código da aplicação não carrega `.env` por conta própria e não usa Supabase Auth.
- A URL de projeto está configurada no código; este relatório omite seu valor.

## 2. Resultados observados na API

| Verificação | Resultado | Interpretação |
|---|---:|---|
| Descoberta OpenAPI do PostgREST | HTTP 401 | O esquema OpenAPI não foi disponibilizado com a credencial usada. |
| Leitura de `information_schema` via PostgREST | HTTP 406 | O schema não foi aceito/exposto pelo endpoint REST; os metadados não puderam ser consultados por essa via. |
| Leitura de `pg_catalog` via PostgREST | HTTP 406 | Estado RLS, índices e políticas não puderam ser consultados por essa via. |
| Linhas visíveis em `categorias` | 4 | Contagem exata retornada pelo endpoint para a credencial atual; sujeita a RLS e permissões. |
| Linhas visíveis em `procedimentos` | 6 | Contagem exata retornada pelo endpoint para a credencial atual; sujeita a RLS e permissões. |
| Procedimentos visíveis sem categoria correspondente | 0 | Verificação dos slugs consultáveis, limitada a 50.000 registros por tabela. |
| Procedimentos visíveis com `categoria_slug` nulo | 0 | Contagem exata retornada pelo endpoint para a credencial atual. |
| Bucket `documentos` | Não listado; consulta direta HTTP 400 | A existência e as configurações do bucket não foram confirmadas. |

As contagens são do conjunto **visível à credencial/role usada pela API**, não necessariamente do total físico do banco. Se RLS restringir linhas, as contagens podem ser menores que o total real.

## 3. Estrutura identificável pelo código

O código de [app/dados.py](./app/dados.py) consulta as seguintes tabelas:

### `categorias`

Campos usados pela aplicação:

- `slug`
- `titulo`
- `descricao`

### `procedimentos`

Campos usados em consultas ou gravações:

- `id`
- `categoria_slug`
- `titulo`
- `resumo`
- `objetivo`
- `como_realizar`
- `pontos_atencao`
- `arquivo_url`

O código relaciona procedimento a categoria comparando `procedimentos.categoria_slug` com `categorias.slug`. Isso confirma o relacionamento **lógico da aplicação**, mas não confirma uma foreign key no banco.

O código envia `como_realizar` e `pontos_atencao` como listas Python. Isso não permite concluir o tipo PostgreSQL real. A aplicação também trata `arquivo_url` como valor opcional; não confirma nulabilidade ou tipo no banco.

### Storage

As rotas em [app/routes.py](./app/routes.py) usam o Storage pelo nome de bucket `documentos`, fazem upload e pedem uma URL pública. A configuração real do bucket e suas policies não foi confirmada.

## 4. Informações não confirmadas

Por falta de acesso de leitura aos catálogos PostgreSQL e à configuração administrativa do Storage, não foi possível confirmar:

- Todas as tabelas existentes no banco, além das tabelas referenciadas pelo código.
- Tipos PostgreSQL, defaults, nulabilidade ou colunas adicionais.
- Chaves primárias, chaves estrangeiras, restrições `UNIQUE`/`CHECK` e regras `ON DELETE`.
- Índices e triggers.
- Estado habilitado/forçado de RLS.
- Policies de leitura, inserção, atualização ou exclusão.
- Existência, visibilidade pública, limite de tamanho e MIME types aceitos pelo bucket `documentos`.
- Policies de objetos do Storage.
- Configuração de usuários, provedores ou papéis no Supabase Auth.

HTTP 401/406/400 não permite distinguir, sozinho, entre configuração de endpoint/schema, permissão insuficiente ou outras restrições do serviço. Não interpretei esses códigos como prova de que uma tabela, policy ou bucket esteja ausente.

## 5. Segurança do aplicativo

- Não há uso de Supabase Auth ou verificação de usuário/papel no código analisado.
- As rotas de escrita `POST /tarefa/novo`, `POST /tarefa/{proc_id}/editar` e `POST /tarefa/{proc_id}/excluir`, em [app/routes.py](./app/routes.py), não exigem autenticação nem checam papéis.
- As leituras também não fazem autorização por usuário ou categoria.
- O efeito real sobre o banco depende das policies Supabase e da credencial configurada no ambiente de deploy, não confirmadas nesta auditoria.
- A chave publishable de fallback está embutida no código. Não equivale a uma chave privilegiada, mas não deve ser tratada como autorização. A ausência de RLS adequado pode expor operações ou linhas.
- A rota de upload aceita arquivos sem validação server-side de MIME type ou limite de tamanho. Esse risco permanece independente do resultado sobre o bucket.
- O código captura exceções de upload e continua o fluxo; falhas podem não ser comunicadas à interface.

## 6. Recomendações para autenticação, papéis e pastas

1. Implementar autenticação com Supabase Auth ou mecanismo equivalente, validando a sessão no servidor em cada rota protegida.
2. Autorizar cada ação no backend. Os papéis aprovados são administrador, editor e colaborador; não confiar em botões ocultos na interface como controle de acesso.
3. Configurar RLS no banco com permissões coerentes e conferir que uma chave publishable não permita escritas anônimas indevidas.
4. Não usar chave privilegiada para contornar RLS. Se for necessária conexão SQL para auditoria, usar credencial de leitura com privilégio mínimo e sem `BYPASSRLS`.
5. Para acesso por pasta, validar autorização da pasta de origem e da pasta de destino em movimentações. Impedir ciclos na árvore e bloquear exclusão de pasta com filhos ou conteúdos.
6. Revisar o Storage junto com o modelo de papéis. Para documentos restritos, preferir bucket privado e emitir acesso após autorização.
7. Antes da migração, confirmar schema, policies, contagens completas e consistência do vínculo categoria/procedimento com acesso de leitura apropriado.

## 7. Como obter os metadados faltantes sem contornar permissões

O cliente REST usado pelo aplicativo não expôs os schemas de catálogo consultados. Para obter os metadados completos, será necessário disponibilizar ao terminal uma conexão PostgreSQL de **somente leitura**, fornecida pelo administrador do projeto e guardada apenas em variável de ambiente local. A role deve ter os privilégios mínimos necessários para ler metadados e executar `SELECT` nas tabelas examinadas, sem `BYPASSRLS` e sem permissões de escrita.

Não usar chave `service_role`, chave secreta ou credencial privilegiada para contornar políticas. Se uma policy impedir a leitura de dados, registrar essa limitação em vez de elevar privilégios.

## 8. Método e garantia de somente leitura

O script temporário usou exclusivamente requisições HTTP `GET` contra PostgREST/OpenAPI e Storage, com chave obtida da configuração existente do projeto sem exibi-la. Não executou SQL de escrita, operações de Storage de escrita, migrations, nem alterou a aplicação ou configurações externas. A verificação estática do script confirmou que as chamadas de rede eram `httpx.get` e que não havia métodos de escrita.

O script temporário será removido ao final; este relatório é o único arquivo novo mantido no projeto.
