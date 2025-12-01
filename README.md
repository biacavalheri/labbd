# 📄 **Sistema de Recrutamento**

## 🧾 **Descrição Geral do Projeto**

Este projeto consiste no desenvolvimento de um **Sistema de Recrutamento completo**, utilizando:

- **Streamlit** como framework de interface web  
- **PostgreSQL** como banco de dados principal  
- **Aiven Cloud** como plataforma de hospedagem do banco  
- Estrutura modular com páginas privadas para administração de vagas e currículos

O sistema implementa de forma simples e funcional o fluxo entre **empresas e candidatos**, possibilitando o gerenciamento de currículos, vagas, candidaturas e níveis de aderência (*match score*).

O sistema pode ser acessado através da URL a seguir:  
https://sistema-recrutamento-labbd.streamlit.app/

---

# 🧠 **Motor de Match Avançado (FTS + Similaridade)**  

O sistema utiliza um **Motor de Match Avançado** baseado em:

### 🔹 1. **Full Text Search (FTS – PostgreSQL)**  
Foi adicionada a coluna `documento_tsv` às tabelas `curriculo` e `vaga`,  
além de triggers automáticos para atualizar o índice FTS sempre que  
um registro é inserido ou atualizado.

O FTS considera:
- título da vaga  
- descrição  
- resumo profissional  
- experiência  

Com pesos diferentes para cada campo.

### 🔹 2. **Similaridade Trigrama (pg_trgm)**  
A extensão `pg_trgm` foi habilitada no PostgreSQL para permitir medir  
a semelhança textual entre:

- resumo do currículo  
- experiência prévia  
- descrição da vaga  
- título da vaga  

Isso permite detectar aderência mesmo quando as palavras não são idênticas.

### 🔹 3. **Match por Skills (interseção N:N)**  
Foi implementado o cálculo proporcional de correspondência entre  
skills da vaga e skills do currículo.

### 🔹 4. **Função match_final()**  
Uma função SQL consolidada unifica todos os fatores:

```
match_final =
    0.50 * match_skills
  + 0.30 * match_trigram
  + 0.20 * match_fts
```

(Returning: 0 a 100%)

### 🔹 5. **View match_engine_view**  
Uma view centraliza todos os matches entre vagas e currículos,  
permitindo ordenação rápida e eficiente.

Essas melhorias tornam o match realista e aplicável em cenários reais.

---

# 🗄️ **Modelagem e Estrutura do Banco de Dados**

O banco de dados foi modelado para garantir **flexibilidade, escalabilidade e normalização**, seguindo princípios da 3FN.

Abaixo estão todas as tabelas essenciais do sistema:

---

## 🟦 **Tabela: vaga**
Armazena informações de vagas cadastradas.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | SERIAL PK | Identificador único |
| titulo | TEXT | Título da vaga |
| descricao | TEXT | Descrição completa |
| empresa | TEXT | Empresa ofertante |
| tipo_contratacao | TEXT | Ex.: CLT, PJ |
| estado | TEXT | UF |
| cidade | TEXT | Cidade |
| salario | NUMERIC | Faixa salarial |

---

## 🟩 **Tabela: curriculo**
Armazena informações detalhadas dos currículos.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | SERIAL PK | Identificador único |
| nome | TEXT | Nome completo |
| email | TEXT | E-mail |
| telefone | TEXT | Telefone |
| formacao | TEXT | Formação acadêmica |
| experiencia | TEXT | Experiência prévia |
| resumo | TEXT | Resumo profissional |
| empresas_previas | TEXT | Histórico de empresas |
| idiomas | TEXT | Lista de idiomas |
| certificacoes | TEXT | Certificações |

---

## 🟧 **Tabela: skill**
Lista de habilidades únicas utilizadas em vagas e currículos.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | SERIAL PK | Identificador único |
| nome | TEXT UNIQUE | Nome da skill |

---

## 🟨 **Tabela: vaga_skill**
Relacionamento N:N entre vagas e skills.

| Campo | Tipo | FK |
|-------|------|----|
| id_vaga | INT | → vaga(id) |
| id_skill | INT | → skill(id) |

---

## 🟪 **Tabela: curriculo_skill**
Relacionamento N:N entre currículos e skills.

| Campo | Tipo | FK |
|-------|------|----|
| id_curriculo | INT | → curriculo(id) |
| id_skill | INT | → skill(id) |

---

## 🟥 **Tabela: candidatura**
Armazena todas as candidaturas realizadas pelos currículos ou oferecidas pelas empresas.

| Campo | Tipo | Descrição |
|-------|------|------------|
| id_curriculo | INT FK | Currículo participante |
| id_vaga | INT FK | Vaga relacionada |
| data_candidatura | TIMESTAMP | Data da operação |

A tabela só aceita **uma candidatura por vaga + currículo**, evitando duplicações.

---

## 🟫 **Tabela: match_score**
Armazena o nível de aderência atribuído manualmente (estrutura legada).

| Campo | Tipo |
|-------|------|
| id_curriculo | INT FK |
| id_vaga | INT FK |
| score | INT CHECK (0–100) |

---

# 🏗️ **Arquitetura do Sistema (Código)**

```
/app.py                     → Arquivo principal da aplicação
/private_pages/
    cadastro_vagas.py       → Cadastro de novas vagas
    cadastro_curriculos.py  → Cadastro de novos currículos
    vagas_abertas.py        → Visualização e candidatura
    curriculos_ativos.py    → Oferecimento e análise de perfis
    match_score_admin.py    → (Legado) gerenciamento manual
    gerenciar_candidatos.py → Inscritos por vaga
    minhas_candidaturas.py  → Histórico do candidato
    db.py                   → Conexão com PostgreSQL
    vagas_publicas.py       → Vagas públicas
    vagas_mapa_publico.py   → Mapa interativo
```

---

# 🔐 **Perfis de Acesso**

### 👤 1. Candidato
- Cadastra currículo  
- Consulta vagas abertas  
- Filtra por localização, skills e contratação  
- Candidata-se  
- Acompanha suas candidaturas  
- Visualiza vagas com maior match  

### 🏢 2. Empregador
- Cadastra vagas  
- Analisa currículos  
- Oferece vagas diretamente  
- Gerencia inscritos  
- Visualiza currículos mais aderentes  

### 🛠️ 3. Administrador
- Supervisiona todo o sistema  
- Gerencia candidaturas  
- Acompanha matches  
- Acesso total às páginas privadas  

---

# 🌐 **Páginas Públicas**

### 📄 `vagas_publicas.py`
Lista todas as vagas abertas sem necessidade de login.

### 🗺 `vagas_mapa_publico.py`
Mapa interativo exibindo a distribuição das vagas.

---

# 🧰 **Tecnologias Utilizadas**

| Tecnologia | Descrição |
|-----------|------------|
| **Streamlit** | Framework web |
| **Python** | Backend |
| **PostgreSQL** | Banco de dados |
| **Aiven Cloud** | Hospedagem |
| **psycopg2-binary** | Driver PostgreSQL |
| **pandas** | Manipulação de dados |
| **GitHub** | Versionamento |

---

# 🚀 **Deploy**

O deploy foi realizado no **Streamlit Cloud**, com dependências definidas em:

```
requirements.txt
```

---

# 👥 **Autores**

Desenvolvido por:

- **Beatriz de Oliveira Cavalheri**  
- **Eduarda Moreira da Silva**  
- **Maysa Marques Santos de Oliveira**
