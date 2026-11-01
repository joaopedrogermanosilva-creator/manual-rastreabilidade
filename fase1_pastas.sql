-- Fase 1: pastas, anexos futuros e vínculo aditivo com procedimentos.
-- Execute no Supabase SQL Editor depois de confirmar que o schema é public.
-- O campo procedimentos.categoria_slug permanece intacto.
-- Este script não altera RLS nem policies; valide acesso às tabelas antes do deploy.

BEGIN;

CREATE TABLE IF NOT EXISTS public.pastas (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    nome text NOT NULL CHECK (btrim(nome) <> ''),
    descricao text NOT NULL DEFAULT '',
    parent_id uuid NULL
        REFERENCES public.pastas (id) ON DELETE RESTRICT,
    ordem integer NOT NULL DEFAULT 0,
    criado_em timestamptz NOT NULL DEFAULT now(),
    atualizado_em timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT pastas_parent_id_not_self CHECK (parent_id IS NULL OR parent_id <> id)
);

ALTER TABLE public.procedimentos
    ADD COLUMN IF NOT EXISTS pasta_id uuid NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'procedimentos_pasta_id_fkey'
          AND conrelid = 'public.procedimentos'::regclass
    ) THEN
        ALTER TABLE public.procedimentos
            ADD CONSTRAINT procedimentos_pasta_id_fkey
            FOREIGN KEY (pasta_id)
            REFERENCES public.pastas (id)
            ON DELETE RESTRICT;
    END IF;
END;
$$;

CREATE INDEX IF NOT EXISTS idx_pastas_parent_ordem
    ON public.pastas (parent_id, ordem, nome);

CREATE INDEX IF NOT EXISTS idx_procedimentos_pasta_id
    ON public.procedimentos (pasta_id);

DO $$
DECLARE
    procedimento_id_type text;
BEGIN
    SELECT format_type(attribute.atttypid, attribute.atttypmod)
    INTO procedimento_id_type
    FROM pg_attribute AS attribute
    WHERE attribute.attrelid = 'public.procedimentos'::regclass
      AND attribute.attname = 'id'
      AND attribute.attnum > 0
      AND NOT attribute.attisdropped;

    IF procedimento_id_type IS NULL THEN
        RAISE EXCEPTION 'Não foi possível determinar o tipo de public.procedimentos.id';
    END IF;

    EXECUTE format(
        'CREATE TABLE IF NOT EXISTS public.anexos (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            procedimento_id %s NOT NULL
                REFERENCES public.procedimentos (id) ON DELETE CASCADE,
            arquivo_url text NOT NULL,
            tipo text NOT NULL,
            nome_original text NOT NULL,
            criado_em timestamptz NOT NULL DEFAULT now()
        )',
        procedimento_id_type
    );
END;
$$;

CREATE INDEX IF NOT EXISTS idx_anexos_procedimento_id
    ON public.anexos (procedimento_id);

COMMIT;
