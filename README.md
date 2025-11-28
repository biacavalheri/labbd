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
    vagas_publicas.py       → Lista vagas abertas sem necessidade de login
    vagas_mapa_publico.py   → Mapa interativo das vagas      
```

---

# 🔐 Perfis de Acesso

O sistema conta com **três perfis distintos**, cada um com permissões e funcionalidades específicas:

### 👤 1. Candidato
- Cadastra e atualiza seu currículo  
- Consulta vagas abertas  
- Filtra vagas por localização, salário, tipo de contratação e skills  
- Candidata-se às vagas  
- Acompanha suas candidaturas  
- Visualiza vagas com maior match score  

### 🏢 2. Empregador
- Cadastra vagas  
- Visualiza currículos disponíveis  
- Oferece vagas diretamente a candidatos  
- Analisa inscritos em cada vaga  
- Define match score entre currículo e vaga  
- Vê currículos mais aderentes  

### 🛠️ 3. Administrador
- Supervisiona todas as vagas e currículos  
- Gerencia candidaturas  
- Controla match score  
- Tem acesso total às rotinas internas de gestão  

---

# 🌐 Páginas Públicas

Além das páginas com login obrigatório, foram adicionadas páginas acessíveis a qualquer visitante:

### 📄 vagas_publicas.py
Lista **todas as vagas abertas** sem necessidade de autenticação.

### 🗺 vagas_mapa_publico.py
Exibe **todas as vagas no mapa interativo**.

Essas páginas permitem que qualquer usuário explore as vagas publicamente, mesmo sem cadastro.

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
