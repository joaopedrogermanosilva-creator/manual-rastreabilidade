CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS idx_procedimentos_titulo_trgm
    ON public.procedimentos USING gin (titulo gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_procedimentos_resumo_trgm
    ON public.procedimentos USING gin (resumo gin_trgm_ops);

CREATE OR REPLACE FUNCTION public.buscar_procedimentos_fuzzy(termo text)
RETURNS SETOF public.procedimentos
LANGUAGE sql
STABLE
AS $$
    SELECT p.*
    FROM public.procedimentos AS p
    WHERE NULLIF(btrim(termo), '') IS NOT NULL
      AND (
          p.titulo ILIKE '%' || btrim(termo) || '%'
          OR COALESCE(p.resumo, '') ILIKE '%' || btrim(termo) || '%'
          OR COALESCE(p.objetivo, '') ILIKE '%' || btrim(termo) || '%'
          OR p.titulo % btrim(termo)
          OR COALESCE(p.resumo, '') % btrim(termo)
          OR btrim(termo) <% p.titulo
          OR btrim(termo) <% COALESCE(p.resumo, '')
      )
    ORDER BY GREATEST(
        similarity(COALESCE(p.titulo, ''), btrim(termo)),
        similarity(COALESCE(p.resumo, ''), btrim(termo)),
        similarity(COALESCE(p.objetivo, ''), btrim(termo)),
        word_similarity(btrim(termo), COALESCE(p.titulo, '')),
        word_similarity(btrim(termo), COALESCE(p.resumo, ''))
    ) DESC, p.id;
$$;
