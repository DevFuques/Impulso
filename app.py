import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import os

os.system('cls' if os.name == 'nt' else 'clear')

# Função para gerar hash da senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Checagem de bibliotecas MySQL
try:
    import mysql.connector as mysql
    print("✅ Usando mysql-connector-python")
except ImportError:
    try:
        import pymysql as mysql
        print("✅ Usando PyMySQL")
    except ImportError:
        print("❌ Nenhuma biblioteca MySQL encontrada!")
        print("👉 Execute o comando abaixo para instalar todas as dependências:")
        print("   pip install -r requirements.txt")
        exit(1) 

# Função de conexão
def conectar():
    return mysql.connect(
        host="localhost",
        user="fernando",        # substitua pelo seu usuário do MySQL
        password="nandocafu",   # substitua pela sua senha do MySQL   
        database="academia"
    )

# Cria banco e tabelas
def inicializa_banco():
    conexao = mysql.connect(
        host="localhost",
        user="fernando",
        password="nandocafu"
    )
    cursor = conexao.cursor()
    cursor.execute("create database if not exists academia")
    cursor.execute("USE academia")

    cursor.execute("""
        create table if not exists pessoas (
            id int auto_increment primary key, 
            nome varchar(255),
            idade int,
            peso float
        )
    """)

    cursor.execute("""
        create table if not exists usuarios(
            id int auto_increment primary key,
            usuario varchar(50) unique not null,
            senha varchar(64) not null,
            tipo varchar(20) not null default 'usuario'
        )
    """)
    
    # cria admin padrão se não existir
    cursor.execute("select count(*) from usuarios")
    if cursor.fetchone()[0] == 0:
        senha_hash = hash_senha("admin")
        cursor.execute(
            "insert into usuarios (usuario, senha, tipo) values (%s, %s, %s)",
            ("admin", senha_hash, "admin")
        )
        print("⭐ Usuário admin criado (usuario: admin | senha: admin)")

    conexao.commit()
    print("✅ BANCO/TABELAS CRIADOS")
    cursor.close()
    conexao.close()
    
# Funções do sistema
def login(usuario, senha):
    conexao = conectar()
    cursor = conexao.cursor()
    senha_hash = hash_senha(senha)
    cursor.execute("select usuario, tipo from usuarios where usuario=%s and senha=%s", (usuario, senha_hash))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado

def cadastrar_usuario():
    conexao = conectar()
    cursor = conexao.cursor()
    usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")
    senha_hash = hash_senha(senha)
    tipo = input("Tipo de usuário (admin/usuario): ").lower()
    if tipo not in ["admin", "usuario"]:
        tipo = "usuario"
    try:
        cursor.execute("insert into usuarios (usuario, senha, tipo) values (%s, %s, %s)", 
                       (usuario, senha_hash, tipo))
        conexao.commit()
        print(f"✅ Usuário {usuario} cadastrado como {tipo}!")
    except mysql.Error as e:
        print(f"❌ Erro: {e}")
    cursor.close()
    conexao.close()
  
def cadastrar_pessoas():
    conexao = conectar()
    cursor = conexao.cursor()
    nome = input("Digite o nome: ")
    idade = int(input("Digite a idade: "))
    peso = float(input("Digite o peso: "))
    sql = "insert into pessoas (nome, idade, peso) values (%s, %s, %s)"
    cursor.execute(sql, (nome, idade, peso))
    conexao.commit()
    print("✅ PESSOA CADASTRADA")
    cursor.close()
    conexao.close()

def mostrar_medias():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("select avg(idade), avg(peso) from pessoas")
    media_idade, media_peso = cursor.fetchone()
    print(f"\nMédia de idade: {media_idade:.2f} anos")
    print(f"Média de peso: {media_peso:.2f} kg\n")
    cursor.close()
    conexao.close()
    
def exibir_tab_pes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("select * from pessoas")
    linhas = cursor.fetchall()
    if linhas:
        print("\n=== PESSOAS CADASTRADAS ===")
        for linha in linhas:
            print(f"| ID: {linha[0]} | Nome: {linha[1]} | Idade: {linha[2]} | Peso: {linha[3]} |")
    else:
        print("\n❌ Nenhuma pessoa foi cadastrada!")
    cursor.close()
    conexao.close()
    
def exibir_tab_user():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("select * from usuarios")
    linhas = cursor.fetchall()
    if linhas:
        print("\n=== USUÁRIOS CADASTRADOS ===")
        for linha in linhas:
            print(f"| ID: {linha[0]} | Usuário: {linha[1]} | Tipo: {linha[3]} |")
    else:
        print("\n❌ Nenhum usuário foi cadastrado!")
    cursor.close()
    conexao.close()
    
def deletar_cadastro():
    conexao = conectar()
    cursor = conexao.cursor()
    id_pessoa = int(input("Digite o ID da pessoa a ser deletada: "))
    sql = "delete from pessoas where id = %s"
    cursor.execute(sql, (id_pessoa,))
    conexao.commit()
    if cursor.rowcount > 0:
        print("\n✅ CADASTRO DELETADO")
    else:
        print("\n❌ ID não encontrado!")
    cursor.close()
    conexao.close()

def deletar_usuario():
    conexao = conectar()
    cursor = conexao.cursor()
    id_usuario = int(input("Digite o ID do usuario a ser deletado: "))
    sql = "delete from usuarios where id = %s"
    cursor.execute(sql, (id_usuario,))
    conexao.commit()
    if cursor.rowcount > 0:
        print("\n✅ USUÁRIO DELETADO")
    else:
        print("\n❌ ID não encontrado!")
    cursor.close()
    conexao.close()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Impulso")
        self.tela_login()
        root.geometry("400x300")
        
    def tela_login(self):
        # Limpar tela
        for widget in self.root.winfo_children():
            widget.destroy()
            
        tk.Label(self.root, text="Login", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.root, text="Usuário:").pack()
        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.pack()
        
        tk.Label(self.root, text="Senha:").pack()
        self.entry_senha = tk.Entry(self.root, show="*")
        self.entry_senha.pack()
        
        tk.Button(self.root, text="Entrar", command=self.fazer_login).pack(pady=10)
        
    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        resultado = login(usuario, senha)
        
        if resultado:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {resultado[0]} ({resultado[1]})!")
            self.tipo_usuario = resultado[1]
            self.menu_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")
            
    def menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        tk.Label(self.root, text="Menu Principal", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Cadastrar Pessoa", command=self.tela_cadastro_pessoa).pack(pady=5)
        tk.Button(self.root, text="Exibir Pessoas", command=self.tela_exibir_pessoas).pack(pady=5)
        tk.Button(self.root, text="Mostrar Médias", command=lambda: messagebox.showinfo("Médias", "Tela médias")).pack(pady=5)
        
        if self.tipo_usuario == "admin":
            tk.Button(self.root, text="Cadastrar Usuário", command=self.tela_cadastrar_usuario).pack(pady=5)
            tk.Button(self.root, text="Exibir Usuários", command=self.tela_exibir_usuarios).pack(pady=5)
            
        tk.Button(self.root, text="Sair", command=self.tela_login).pack(pady=10)
        
    def tela_cadastro_pessoa(self):
        janela = tk.Toplevel(self.root)
        janela.title("Cadastrar Pessoa")

        tk.Label(janela, text="Nome:").pack(pady=5)
        entry_nome = tk.Entry(janela)
        entry_nome.pack()

        tk.Label(janela, text="Idade:").pack(pady=5)
        entry_idade = tk.Entry(janela)
        entry_idade.pack()

        tk.Label(janela, text="Peso:").pack(pady=5)
        entry_peso = tk.Entry(janela)
        entry_peso.pack()

        def salvar():
            nome = entry_nome.get()
            try:
                idade = int(entry_idade.get())
                peso = float(entry_peso.get())
            except ValueError:
                messagebox.showerror("Erro", "Idade deve ser número inteiro e Peso deve ser número decimal.")
                return

            conexao = conectar()
            cursor = conexao.cursor()
            sql = "INSERT INTO pessoas (nome, idade, peso) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nome, idade, peso))
            conexao.commit()
            cursor.close()
            conexao.close()

            messagebox.showinfo("Sucesso", f"Pessoa '{nome}' cadastrada com sucesso!")
            janela.destroy()

        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)
        tk.Button(janela, text="Cancelar", command=janela.destroy).pack()
        
    def tela_exibir_pessoas(self):
        janela = tk.Toplevel(self.root)
        janela.title("Pessoas Cadastradas")
        janela.geometry("500x350")

        colunas = ("ID", "Nome", "Idade", "Peso")
        self.tree_pessoas = ttk.Treeview(janela, columns=colunas, show="headings")
        self.tree_pessoas.pack(fill="both", expand=True, pady=10)

        # Definir cabeçalhos
        self.tree_pessoas.heading("ID", text="ID")
        self.tree_pessoas.heading("Nome", text="Nome")
        self.tree_pessoas.heading("Idade", text="Idade")
        self.tree_pessoas.heading("Peso", text="Peso")

        # Ajustar larguras
        self.tree_pessoas.column("ID", width=50)
        self.tree_pessoas.column("Nome", width=150)
        self.tree_pessoas.column("Idade", width=100)
        self.tree_pessoas.column("Peso", width=100)

        # Botão de deletar 
        btn_deletar = tk.Button(janela, text="Deletar Selecionado", command=self.deletar_pessoa)
        btn_deletar.pack(pady=5)

        self.carregar_pessoas()
       
    def carregar_pessoas(self):
        """Carrega os registros do banco na Treeview"""
        for item in self.tree_pessoas.get_children():
            self.tree_pessoas.delete(item)

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM pessoas")
        linhas = cursor.fetchall()
        cursor.close()
        conexao.close()

        for linha in linhas:
            self.tree_pessoas.insert("", tk.END, values=linha)

    def deletar_pessoa(self):
        """Deleta a pessoa selecionada na Treeview"""
        selecionado = self.tree_pessoas.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma pessoa para deletar.")
            return

        item = self.tree_pessoas.item(selecionado)
        pessoa_id = item["values"][0]

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM pessoas WHERE id = %s", (pessoa_id,))
        conexao.commit()
        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Pessoa deletada com sucesso!")
        self.carregar_pessoas()
        
    def tela_cadastrar_usuario(self):
        janela = tk.Toplevel(self.root)
        janela.title("Cadastrar Usuário")
        janela.geometry("350x250")

        tk.Label(janela, text="Usuário:").pack(pady=5)
        entry_usuario = tk.Entry(janela)
        entry_usuario.pack()

        tk.Label(janela, text="Senha:").pack(pady=5)
        entry_senha = tk.Entry(janela, show="*")
        entry_senha.pack()

        tk.Label(janela, text="Tipo:").pack(pady=5)
        combo_tipo = ttk.Combobox(janela, values=["usuario", "admin"], state="readonly")
        combo_tipo.current(0)  # valor padrão = usuario
        combo_tipo.pack()

        def salvar_usuario():
            usuario = entry_usuario.get().strip()
            senha = entry_senha.get().strip()
            tipo = combo_tipo.get()

            if not usuario or not senha:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
                return

            senha_hash = hash_senha(senha)

            conexao = conectar()
            cursor = conexao.cursor()

            try:
                cursor.execute("INSERT INTO usuarios (usuario, senha, tipo) VALUES (%s, %s, %s)",
                            (usuario, senha_hash, tipo))
                conexao.commit()
                messagebox.showinfo("Sucesso", f"Usuário '{usuario}' cadastrado como {tipo}!")
                janela.destroy()
            except mysql.Error as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")
            finally:
                cursor.close()
                conexao.close()

        tk.Button(janela, text="Salvar", command=salvar_usuario).pack(pady=10)
        tk.Button(janela, text="Cancelar", command=janela.destroy).pack()

    def tela_exibir_usuarios(self):
        janela = tk.Toplevel(self.root)
        janela.title("Usuários Cadastrados")
        janela.geometry("500x350")

        colunas = ("ID", "Usuário", "Tipo")
        self.tree_usuarios = ttk.Treeview(janela, columns=colunas, show="headings")
        self.tree_usuarios.pack(fill="both", expand=True, pady=10)

        # Cabeçalhos
        self.tree_usuarios.heading("ID", text="ID")
        self.tree_usuarios.heading("Usuário", text="Usuário")
        self.tree_usuarios.heading("Tipo", text="Tipo")

        # Larguras
        self.tree_usuarios.column("ID", width=50)
        self.tree_usuarios.column("Usuário", width=200)
        self.tree_usuarios.column("Tipo", width=100)

        # Botão deletar
        btn_deletar = tk.Button(janela, text="Deletar Selecionado", command=self.deletar_usuario)
        btn_deletar.pack(pady=5)

        self.carregar_usuarios()

    def carregar_usuarios(self):
        """Carrega usuários no Treeview"""
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, usuario, tipo FROM usuarios")
        linhas = cursor.fetchall()
        cursor.close()
        conexao.close()

        for linha in linhas:
            self.tree_usuarios.insert("", tk.END, values=linha)

    def deletar_usuario(self):
        """Deleta usuário selecionado"""
        selecionado = self.tree_usuarios.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um usuário para deletar.")
            return

        item = self.tree_usuarios.item(selecionado)
        usuario_id = item["values"][0]

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        conexao.commit()
        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Usuário deletado com sucesso!")
        self.carregar_usuarios()
        
if __name__ == "__main__":
    inicializa_banco()
    root = tk.Tk()
    app_instance = App(root)
    root.mainloop()
    