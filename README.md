<p align= "center">
  <img width="920" height="300" alt="impulsoBannerMaior" src="https://github.com/user-attachments/assets/d3385862-5cce-4adb-9fe6-6fdfca8b4ed7" />
</p>

# Impulso — *Impulsionando sua gestão*
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

Um sistema de **gestão com interface gráfica (Tkinter)** integrado ao **MySQL**.  
Criado para praticar conceitos de banco de dados, CRUD, autenticação segura com hash SHA-256 e interface desktop moderna em Python.  

---

## ✨ Funcionalidades
- 🏗️ Criação automática do banco e tabelas
- 👤 Cadastro de usuários (admin/usuário) e pessoas
- 🔑 Login seguro com hash SHA-256
- 📊 Cálculo da média de idade e peso cadastrados
- 📋 Listagem de pessoas e usuários
- 🗑️ Deleção e edição de registros
- 🔄 Suporte a mysql-connector-python e PyMySQL
- 🎨 Interface gráfica com Tkinter (tema preto/cinza/amarelo)
- 🔒 Garantia de existência de usuário admin na primeira execução

---

## 🛠 Tecnologias utilizadas
- [Python 3](https://www.python.org/)
- [Tkinter (GUI)](https://docs.python.org/3/library/tkinter.html)
- [MySQL](https://www.mysql.com/)
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
- [PyMySQL](https://pypi.org/project/PyMySQL/)
- [hashlib](https://docs.python.org/pt-br/3.13/library/hashlib.html)
  
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
- API ViaCEP

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
- cep (varchar)
- logradouro (varchar)
- bairro (varchar)
- cidade (varchar)
- estado (varchar)

---

## ⚙️ Pré-requisitos

Antes de executar o sistema, verifique se você possui o Python 3.10 ou superior instalado na sua máquina.

### 🔍 Como verificar a versão do Python

No terminal/cmd, digite:
```bash
python --version
```
ou (em algumas distribuições Linux):
```bash
python3 --version
```
Se o resultado mostrar algo como:
```nginx
Python 3.10.12
```
✅ Você já está pronto para continuar.

### 🐍 Instalando o Python

Caso não tenha o Python instalado, siga o guia oficial de acordo com o seu sistema operacional:

- Windows
  - Baixe o instalador no site oficial:
    👉 https://www.python.org/downloads/windows/
  - Durante a instalação, marque a opção "Add Python to PATH".
- Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```
---

## ⚙️ Como executar

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/DevFuques/Impulso.git
```
```bash
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
Edite o arquivo db.py com o **usuário** e **senha** do seu MySQL.
<img width="521" height="307" alt="image" src="https://github.com/user-attachments/assets/353e7297-0f25-4562-a16e-2905f66e37b1" />

### 6️⃣ Executar o software
```bash
python3 app.py
```
Ou
```bash
python app.py
```

💡 **Nota:** na primeira execução, o sistema cria um usuário admin padrão, caso ele já exista sera informado.  

<p align="center">
  <img width="274" height="66" alt="image" src="https://github.com/user-attachments/assets/534fd2c4-e6d2-458b-842d-9f281e27df16" />
</p>

---

## 📸 Demonstração
<p align= "center">
  <img width="420" height="353" alt="Captura de tela de 2025-08-31 14-30-56" src="https://github.com/user-attachments/assets/6b36f673-a93e-4deb-9ecf-09eb93712652" />
  <img width="418" height="420" alt="image" src="https://github.com/user-attachments/assets/485e5eec-3c05-4543-978b-502d135e9546" />
</p>

---

## 📄 Documentação de infraestrutura e integração/API
### 🖥️ Requisitos de Infraestrutura

- Hardware mínimo recomendado:
  - CPU: 2 núcleos
  - RAM: 4 GB
  - Armazenamento: 200 MB livres
  - Sistema Operacional: Windows 10+, Linux (Ubuntu/Debian 20.04+), macOS 10.15+

- Software necessário:
  - Python 3.10 ou superior
  - MySQL 8+ ou MariaDB
  - pip para instalar dependências
  - Bibliotecas Python: mysql-connector-python, PyMySQL, hashlib, tkinter

### 🌐 Integração com API externa

O sistema utiliza a API ViaCEP para buscar endereços automaticamente a partir do CEP informado.

- Como funciona:
 1. O usuário digita o CEP no formulário de cadastro de pessoas.
 2. O sistema faz uma requisição HTTP para a API ViaCEP utilizando urllib.request.
 3. Os dados retornados (logradouro, bairro, cidade, estado) são preenchidos automaticamente nos campos do formulário.

---

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
