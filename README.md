<img width="1536" height="1024" alt="impulso" src="https://github.com/user-attachments/assets/702576fe-00bb-495f-94bd-cefb9d774214" />

# *Onde a tecnologia encontra a performance.*
Este é um sistema simples de **gestão de academias** utilizando Python + MySQL.
O projeto foi criado para praticar conceitos de banco de dados, CRUD básico e integração do Python com diferentes drivers MySQL.

---

## ✨ Funcionalidades Gerais
- 🏗️ Criação automática do banco e tabela caso não existam
- 👤 Cadastro de novas pessoas e usuários
- 📊 Cálculo da média de idade e peso cadastrados
- 📋 Exibição de todas as pessoas registradas
- 🔄 Compatibilidade com mysql-connector-python e PyMySQL 

---

## 🛠 Tecnologias utilizadas
- [Python 3](https://www.python.org/)
- [MySQL](https://www.mysql.com/)
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
- [PyMySQL](https://pypi.org/project/PyMySQL/)
- [hashlib](https://docs.python.org/pt-br/3.13/library/hashlib.html)
- [os](https://docs.python.org/pt-br/3.13/library/os.html)
  
---
## 📚 Contexto do projeto
Este projeto foi desenvolvido como exercício prático para consolidar o aprendizado em:
- Conexão do Python com MySQL
- Manipulação de tabelas e registros
- Estruturação de um menu interativo no terminal
- Uso de try/except para lidar com múltiplos drivers

Durante as minha aulas no SENAI, foi dado aos alunos um desafio de criarem um código que unisse Banco de dados com alguma linguagem e que fosse criado um software funcional.  
Inspirado pelo desafio e com um pouco de pesquisa, criei este programa adicionando funcionalidades extras além do que havia sido solicitado pela professora..

---

## 📌 Funcionalidades

- Login com senha hash SHA-256 (não salva senhas em texto puro 🚫).
- Usuários com dois tipos de permissões:
  - Admin → pode cadastrar novos usuários, além de todas as funções normais.
  - Usuário comum → pode apenas gerenciar pessoas.
- Cadastro de pessoas (nome, idade, peso).
- Exibição de todas as pessoas cadastradas.
- Cálculo de médias de idade e peso.
- Exclusão de cadastros.

---

### 🖥️ Estrutura do banco

- usuarios
  - id (int, auto_increment, PK)
  - usuario (varchar, único)
  - senha (varchar)
  - tipo (admin/usuario)

- pessoas
  - id (int, auto_increment, PK)
  - nome (varchar)
  - idade (int)
  - peso (float)

---

## 🚀 Como executar

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/DevFuques/Impulso.git
cd Impulso
```
### 2️⃣ Criar um ambiente virtual
```bash
python3 -m venv venv
```
### 3️⃣ Ativar o ambiente virtual

#### - Linux/macOS
```bash
  source venv/bin/activate
```
#### - Windows
```bash
  venv\Scripts\activate
```
### 4️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```
### 5️⃣ Configurando o MySQL
Troque o user e a password do código para os que você usa no seu MySQL

<img width="521" height="307" alt="image" src="https://github.com/user-attachments/assets/353e7297-0f25-4562-a16e-2905f66e37b1" />

### 6️⃣ Executar o software
```bash
python3 app.py
```
---

## 📸 Demonstração


---

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
