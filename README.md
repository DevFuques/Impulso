<p align= "center">
  <img width="920" height="300" alt="impulsoBannerMaior" src="https://github.com/user-attachments/assets/d3385862-5cce-4adb-9fe6-6fdfca8b4ed7" />
</p>

# Impulso — *Impulsionando sua gestão*
Um sistema simples de **gestão** desenvolvido em **Python + MySQL**, criado para praticar conceitos de banco de dados, CRUD e integração com diferentes drivers MySQL.  

---

## ✨ Funcionalidades
- 🏗️ Criação automática do banco e tabelas  
- 👤 Cadastro de usuários e pessoas  
- 🔑 Login seguro com hash SHA-256  
- 📊 Cálculo da média de idade e peso cadastrados  
- 📋 Listagem de pessoas e usuários  
- 🔄 Suporte a **mysql-connector-python** e **PyMySQL** 

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
Inspirado pelo desafio e com um pouco de pesquisa, criei este programa adicionando funcionalidades extras além do que havia sido solicitado pela professora.

---

## 📌 Especificações
- Login seguro com **hash SHA-256** (sem senhas em texto puro 🚫)  
- Dois tipos de usuário:
  - **Admin** → pode cadastrar novos usuários e realizar todas as funções  
  - **Usuário comum** → pode apenas gerenciar pessoas  
- CRUD completo de **usuários** e **pessoas**  
- Cadastro de pessoas (nome, idade, peso)  
- Listagem e cálculo de médias  

---

## 🖥️ Estrutura do banco
**Tabela: usuarios**
- id (int, PK, auto_increment)  
- usuario (varchar, único)  
- senha (varchar)  
- tipo (enum: admin/usuario)  

**Tabela: pessoas**
- id (int, PK, auto_increment)  
- nome (varchar)  
- idade (int)  
- peso (float)  

---

## ⚙️ Como executar

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
Ou
```bash
python app.py
```

💡 **Nota:** na primeira execução, o sistema cria um usuário admin padrão.  

<p align="center">
  <img width="467" height="119" src="https://github.com/user-attachments/assets/f50fe770-8f86-4fcf-87b0-ae713d31f6d0" alt="Usuário padrão">
</p>

---

## 📸 Demonstração


---

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
