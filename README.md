# 📄 **Sistema de Recrutamento**

## 🧾 **Descrição Geral do Projeto**

Este projeto consiste no desenvolvimento de um **Sistema de Recrutamento completo**, utilizando:

- **Streamlit** como framework de interface web  
- **PostgreSQL** como banco de dados principal  
- **Aiven Cloud** como plataforma de hospedagem do banco  
- Estrutura modular com páginas privadas para administração de vagas e currículos

O sistema implementa de forma simples e funcional o fluxo entre **empresas e candidatos**, possibilitando o gerenciamento de currículos, vagas, candidaturas e níveis de aderência (*match score*).

O sistema pode ser acessado através da URL a seguir: https://sistema-recrutamento-labbd.streamlit.app/

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
Armazena o nível de aderência entre um currículo e uma vaga, atribuído manualmente pelo admin.

| Campo | Tipo |
|-------|------|
| id_curriculo | INT FK |
| id_vaga | INT FK |
| score | INT CHECK (0–100) |

Usada para exibir automaticamente os **2 maiores matches** de cada vaga ou currículo.

---

# 🏗️ **Arquitetura do Sistema (Código)**

```
/app.py                     → Arquivo principal da aplicação
/private_pages/
    cadastro_vagas.py       → Cadastro de novas vagas
    cadastro_curriculos.py  → Cadastro de novos currículos
    vagas_abertas.py        → Visualização e candidatura a vagas
    curriculos_ativos.py    → Visualização e oferta de vagas
    match_score_admin.py    → Gerenciamento do match score
    gerenciar_candidatos.py → Lista de candidatos de cada vaga
    minhas_candidaturas.py  → Lista de candidaturas realizadas
    db.py                   → Conexão segura com o PostgreSQL
```

---

# 🔐 **Sistema de Login**

Existem dois perfis principais:

---

## 👔 **admin_vagas**

### Funcionalidades:
- Cadastrar novas vagas  
- Selecionar uma vaga para gerenciamento  
- Visualizar currículos disponíveis  
- Oferecer vaga a candidatos  
- Ver candidatos inscritos  
- Atribuir match score 0–100  
- Ver os dois currículos mais aderentes  

---

## 👤 **admin_curriculos**

### Funcionalidades:
- Cadastrar novos currículos  
- Selecionar um currículo para gerenciamento  
- Visualizar vagas abertas  
- Candidatar currículo às vagas  
- Ver histórico de candidaturas  
- Ver as duas vagas com maior match score  

---

# 🔄 **Fluxo Operacional**

## Para admin_curriculos:
1. Seleciona um currículo  
2. Filtra vagas por palavras‑chave, localização, tipo de contratação, salário etc.  
3. Clica em *Candidatar-se*  
4. Consulta todas as candidaturas realizadas  

## Para admin_vagas:
1. Seleciona uma vaga no topo da página  
2. Filtra currículos  
3. Visualiza detalhes e oferece a vaga a um candidato  
4. Atribui match score  
5. Visualiza todos os inscritos na vaga  

---

# 🧰 **Tecnologias Utilizadas**

| Tecnologia | Descrição |
|-----------|------------|
| **Streamlit** | Framework web |
| **Python** | Backend |
| **PostgreSQL** | Banco de dados |
| **Aiven Cloud** | Hospedagem gerenciada |
| **psycopg2-binary** | Conexão com o banco |
| **pandas** | Manipulação de dados |
| **GitHub** | Versionamento e deploy |

---

# 🚀 **Deploy**

O deploy foi realizado no **Streamlit Cloud**, com dependências especificadas em:

```
requirements.txt
```

---

# 👥 **Autores**

Desenvolvido por:

- **Beatriz de Oliveira Cavalheri**  
- **Eduarda Moreira da Silva**  
- **Maysa Marques Santos de Oliveira**
