# **Sistema de Recrutamento**

## 🧾 **Descrição Geral do Projeto**

Este projeto consiste no desenvolvimento de um **Sistema de Recrutamento completo**, utilizando:

- **Streamlit** como framework de interface web  
- **PostgreSQL** como banco de dados principal  
- **Aiven Cloud** como plataforma de hospedagem do banco  
- Estrutura modular com páginas privadas para administração de vagas e currículos

O sistema implementa de forma simples e funcional o fluxo entre **empresas e candidatos**, possibilitando o gerenciamento de currículos, vagas, candidaturas e níveis de aderência (*match score*).

O trabalho foi concebido como atividade prática da disciplina **Laboratório de Banco de Dados**.

---

# 🏗️ **Arquitetura do Sistema**

O projeto é estruturado da seguinte forma:

```
/app.py                     → Arquivo principal da aplicação
/private_pages/
    cadastro_vagas.py       → Cadastro de novas vagas
    cadastro_curriculos.py  → Cadastro de novos currículos
    vagas_abertas.py        → Visualização e candidatura a vagas
    curriculos_ativos.py    → Visualização e oferta de vagas
    match_score_admin.py    → Gerenciamento do match score
    gerenciar_candidatos.py → Lista de candidatos de cada vaga
    minhas_candidaturas.py  → Lista de candidaturas de um currículo
    db.py                   → Conexão com PostgreSQL (Aiven Cloud)
```

---

# 🧮 **Banco de Dados**

As tabelas utilizadas no sistema são:

- **vaga**  
- **curriculo**  
- **skill**  
- **vaga_skill**  
- **curriculo_skill**  
- **candidatura**  
- **match_score**

---

# 🔐 **Sistema de Login**

Existem dois perfis de acesso ao sistema:

## 👔 **admin_vagas**
Acesso destinado a administradores responsáveis por vagas.

### Funcionalidades:
- Cadastrar novas vagas  
- Visualizar currículos disponíveis  
- Oferecer vagas diretamente a candidatos  
- Visualizar candidatos inscritos em cada vaga (via tabela *candidatura*)  
- Gerenciar níveis de aderência (*match score*)  
- Utilizar filtros de busca avançados para seleção de candidatos

---

## 👤 **admin_curriculos**
Acesso destinado a administradores responsáveis por currículos.

### Funcionalidades:
- Cadastrar novos currículos  
- Visualizar vagas abertas  
- Candidatar currículos às vagas  
- Ver histórico de candidaturas realizadas  
- Utilizar filtros de busca avançados para seleção de vagas

---

# 🔄 **Fluxo de Funcionamento**

### 📌 **Fluxo para admin_curriculos**
1. Seleciona um currículo na interface  
2. Pesquisa vagas usando filtros (palavras-chave, localidade, tipo de contratação, faixa salarial etc.)  
3. Visualiza detalhes e realiza candidatura  
4. Consulta suas candidaturas na página *Minhas Candidaturas*

### 📌 **Fluxo para admin_vagas**
1. Seleciona uma vaga a ser administrada  
2. Pesquisa currículos usando filtros  
3. Visualiza detalhes e oferece a vaga ao candidato desejado  
4. Gerencia match score manualmente  
5. Acompanha os candidatos inscritos via página *Gerenciar Candidatos*

---

# 🧰 **Tecnologias Utilizadas**

| Tecnologia | Finalidade |
|-----------|------------|
| **Streamlit** | Interface web |
| **PostgreSQL** | Banco de dados relacional |
| **Aiven Cloud** | Hospedagem do banco PostgreSQL |
| **psycopg2-binary** | Conexão Python ↔ PostgreSQL |
| **Python 3.10+** | Linguagem principal do backend |

---

# 🚀 **Deploy**

O deploy foi realizado utilizando o **Streamlit Cloud**, com dependências declaradas em:

```
requirements.txt
```

Incluindo:

```
streamlit
psycopg2-binary
pandas
```

---

# 👥 **Autores**

Desenvolvido por:

- **Beatriz de Oliveira Cavalheri**  
- **Eduarda Moreira da Silva**  
- **Maysa Marques Santos de Oliveira**
