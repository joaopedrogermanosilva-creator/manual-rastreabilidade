CREATE TABLE IF NOT EXISTS public.configuracoes (
    chave TEXT PRIMARY KEY,
    valor TEXT NOT NULL,
    atualizado_em TIMESTAMPTZ DEFAULT now()
);

GRANT ALL ON public.configuracoes TO anon, authenticated, service_role;
