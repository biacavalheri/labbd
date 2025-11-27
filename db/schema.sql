CREATE TABLE skill (
    id SERIAL PRIMARY KEY,
    nome TEXT UNIQUE NOT NULL
);

CREATE TABLE vaga (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    empresa TEXT NOT NULL,
    tipo_contratacao TEXT NOT NULL,
    estado TEXT NOT NULL,
    cidade TEXT NOT NULL,
    salario NUMERIC(12,2)
);

CREATE TABLE vaga_skill (
    id_vaga INT NOT NULL REFERENCES vaga(id) ON DELETE CASCADE,
    id_skill INT NOT NULL REFERENCES skill(id) ON DELETE CASCADE,
    PRIMARY KEY (id_vaga, id_skill)
);

CREATE TABLE curriculo (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL,
    formacao TEXT NOT NULL,
    experiencia TEXT NOT NULL,
    resumo TEXT NOT NULL,
    empresas_previas TEXT,
    idiomas TEXT,
    certificacoes TEXT
);

CREATE TABLE curriculo_skill (
    id_curriculo INT NOT NULL REFERENCES curriculo(id) ON DELETE CASCADE,
    id_skill INT NOT NULL REFERENCES skill(id) ON DELETE CASCADE,
    PRIMARY KEY (id_curriculo, id_skill)
);

CREATE TABLE candidatura (
    id SERIAL PRIMARY KEY,
    id_curriculo INT NOT NULL REFERENCES curriculo(id) ON DELETE CASCADE,
    id_vaga INT NOT NULL REFERENCES vaga(id) ON DELETE CASCADE,
    origem VARCHAR(20) NOT NULL CHECK (origem IN ('candidato', 'empresa')),
    data TIMESTAMP DEFAULT NOW()
);

CREATE TABLE match_score (
    id_curriculo INT REFERENCES curriculo(id),
    id_vaga INT REFERENCES vaga(id),
    score INT CHECK (score BETWEEN 0 AND 100),
    PRIMARY KEY (id_curriculo, id_vaga)
);
