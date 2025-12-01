------------------------------------------------------------
--  FULL TEXT SEARCH - SETUP COMPLETO
------------------------------------------------------------


------------------------------------------------------------
-- 1. ADICIONAR COLUNAS TSVECTOR (SE NÃO EXISTIREM)
------------------------------------------------------------
ALTER TABLE curriculo 
    ADD COLUMN IF NOT EXISTS documento_tsv tsvector;

ALTER TABLE vaga 
    ADD COLUMN IF NOT EXISTS documento_tsv tsvector;


------------------------------------------------------------
-- 2. POPULAR TSVECTOR PARA DADOS EXISTENTES
------------------------------------------------------------
UPDATE curriculo
SET documento_tsv = to_tsvector(
    'portuguese',
      coalesce(nome,'')        || ' '
    || coalesce(formacao,'')    || ' '
    || coalesce(experiencia,'') || ' '
    || coalesce(resumo,'')      || ' '
    || coalesce(empresas_previas,'')
);

UPDATE vaga
SET documento_tsv = to_tsvector(
    'portuguese',
      coalesce(titulo,'')    || ' '
    || coalesce(descricao,'') || ' '
    || coalesce(empresa,'')
);


------------------------------------------------------------
-- 3. CRIAR ÍNDICES GIN (SE NÃO EXISTIREM)
------------------------------------------------------------

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes WHERE indexname = 'idx_curriculo_tsv'
    ) THEN
        CREATE INDEX idx_curriculo_tsv
        ON curriculo USING GIN(documento_tsv);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes WHERE indexname = 'idx_vaga_tsv'
    ) THEN
        CREATE INDEX idx_vaga_tsv
        ON vaga USING GIN(documento_tsv);
    END IF;
END $$;


------------------------------------------------------------
-- 4. FUNÇÃO DO TRIGGER: ATUALIZAR TSVECTOR (CURRÍCULO)
------------------------------------------------------------

CREATE OR REPLACE FUNCTION trg_update_curriculo_tsv()
RETURNS trigger AS $$
BEGIN
    NEW.documento_tsv := to_tsvector(
        'portuguese',
          coalesce(NEW.nome,'')        || ' '
        || coalesce(NEW.formacao,'')    || ' '
        || coalesce(NEW.experiencia,'') || ' '
        || coalesce(NEW.resumo,'')      || ' '
        || coalesce(NEW.empresas_previas,'')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


------------------------------------------------------------
-- 5. TRIGGER (CURRÍCULO)
------------------------------------------------------------

DROP TRIGGER IF EXISTS update_curriculo_tsv ON curriculo;

CREATE TRIGGER update_curriculo_tsv
BEFORE INSERT OR UPDATE ON curriculo
FOR EACH ROW
EXECUTE FUNCTION trg_update_curriculo_tsv();


------------------------------------------------------------
-- 6. FUNÇÃO DO TRIGGER: ATUALIZAR TSVECTOR (VAGA)
------------------------------------------------------------

CREATE OR REPLACE FUNCTION trg_update_vaga_tsv()
RETURNS trigger AS $$
BEGIN
    NEW.documento_tsv := to_tsvector(
        'portuguese',
          coalesce(NEW.titulo,'')    || ' '
        || coalesce(NEW.descricao,'') || ' '
        || coalesce(NEW.empresa,'')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


------------------------------------------------------------
-- 7. TRIGGER (VAGA)
------------------------------------------------------------

DROP TRIGGER IF EXISTS update_vaga_tsv ON vaga;

CREATE TRIGGER update_vaga_tsv
BEFORE INSERT OR UPDATE ON vaga
FOR EACH ROW
EXECUTE FUNCTION trg_update_vaga_tsv();


------------------------------------------------------------
-- 8. VIEW DE MATCH AUTOMÁTICO
------------------------------------------------------------

CREATE OR REPLACE VIEW match_score_automatico AS
SELECT
    c.id AS id_curriculo,
    v.id AS id_vaga,
    ts_rank_cd(
        v.documento_tsv,
        plainto_tsquery('portuguese', c.documento_tsv::text)
    ) * 100 AS match_score
FROM curriculo c
CROSS JOIN vaga v;


------------------------------------------------------------
--  FIM DO SETUP
------------------------------------------------------------
