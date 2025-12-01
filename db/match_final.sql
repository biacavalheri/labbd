CREATE OR REPLACE FUNCTION match_final(curriculo_id INT, vaga_id INT)
RETURNS FLOAT AS $$
DECLARE
    s1 FLOAT; -- skills
    s2 FLOAT; -- trigram
    s3 FLOAT; -- fts
    resultado FLOAT;
BEGIN
    s1 := match_skills(curriculo_id, vaga_id);
    s2 := match_trigram(curriculo_id, vaga_id);
    s3 := match_fts(curriculo_id, vaga_id);

    -- pesos
    resultado := 0.50*s1 + 0.30*s2 + 0.20*s3;

    -- CONVERSÃO PARA NUMERIC ANTES DO ROUND
    RETURN ROUND((resultado * 100)::numeric, 2);
END;
$$ LANGUAGE plpgsql;
