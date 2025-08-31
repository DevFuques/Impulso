import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as mysql

from db import conectar
from models.usuarios import hash_senha

class MenuPrincipal:
    def __init__(self, root, tipo_usuario):
        self.root = root
        self.root.title("Impulso - Menu Principal")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="📋 Menu Principal", style="Header.TLabel").pack(pady=15)

        ttk.Button(frame, text="Cadastrar Pessoa", command=self.cadastrar_pessoa).pack(fill="x", pady=5)
        ttk.Button(frame, text="Exibir Pessoas", command=self.exibir_pessoas).pack(fill="x", pady=5)
        ttk.Button(frame, text="Mostrar Médias", command=self.mostrar_medias).pack(fill="x", pady=5)

        if tipo_usuario == "admin":
            self.root.geometry("400x550")
            self.root.resizable(False, False)
            ttk.Separator(frame).pack(fill="x", pady=10)
            ttk.Button(frame, text="Cadastrar Usuário", command=self.cadastrar_usuario).pack(fill="x", pady=5)
            ttk.Button(frame, text="Mostrar Usuários", command=self.mostrar_usuario).pack(fill="x", pady=5)

        ttk.Separator(frame).pack(fill="x", pady=10)
        ttk.Button(frame, text="🚪 Sair", command=self.root.quit).pack(fill="x", pady=5)

    def cadastrar_pessoa(self):
        conexao = conectar()
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

    def exibir_pessoas(self):
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

    def mostrar_medias(self):
        messagebox.showinfo("Médias", "Mostrar médias de idade e peso")

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

    def cadastrar_usuario(self):
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

    def mostrar_usuario(self):
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
    
