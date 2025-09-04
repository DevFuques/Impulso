import tkinter as tk
from tkinter import ttk, messagebox
from ui.pessoas_ui import CadastroPessoaUI, ExibirPessoasUI
from ui.usuarios_ui import UsuariosUI
from db import conectar

class MenuPrincipal:
    def __init__(self, root, tipo_usuario):
        self.root = root
        self.root.title("Impulso - Menu Principal")
        self.root.geometry("400x450")
        self.root.resizable(False, False)

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="📋 Menu Principal", font=("Helvetica", 16, "bold")).pack(pady=15)

        # --- Botões principais ---
        ttk.Button(frame, text="Cadastrar Pessoa", command=self.cadastrar_pessoa).pack(fill="x", pady=5)
        ttk.Button(frame, text="Exibir Pessoas", command=self.exibir_pessoas).pack(fill="x", pady=5)
        ttk.Button(frame, text="Mostrar Médias", command=self.mostrar_medias).pack(fill="x", pady=5)

        # --- Botões para admins ---
        if tipo_usuario == "admin":
            ttk.Separator(frame).pack(fill="x", pady=10)
            ttk.Button(frame, text="Gerenciar Usuários", command=self.gerenciar_usuarios).pack(fill="x", pady=5)

        ttk.Separator(frame).pack(fill="x", pady=10)
        ttk.Button(frame, text="🚪 Sair", command=self.root.quit).pack(fill="x", pady=5)

    # --- Funções ---
    def cadastrar_pessoa(self):
        nova_janela = tk.Toplevel(self.root)
        CadastroPessoaUI(nova_janela)

    def exibir_pessoas(self):
        nova_janela = tk.Toplevel(self.root)
        ExibirPessoasUI(nova_janela)

    def mostrar_medias(self):
        # Conecta ao banco e calcula médias
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT AVG(idade), AVG(peso) FROM pessoas")
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()

        media_idade, media_peso = resultado if resultado else (0, 0)

        # Cria janela
        janela = tk.Toplevel(self.root)
        janela.title("Médias de Idade e Peso")
        janela.geometry("300x180")
        janela.resizable(False, False)

        frame = ttk.Frame(janela, padding=10)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="📊 Médias de Idade e Peso", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Treeview simples para mostrar as médias
        colunas = ("Campo", "Média")
        tree = ttk.Treeview(frame, columns=colunas, show="headings", height=2)
        tree.heading("Campo", text="Campo")
        tree.heading("Média", text="Média")
        tree.column("Campo", width=120, anchor="center")
        tree.column("Média", width=120, anchor="center")
        tree.pack(expand=True, fill="both", pady=10)

        # Inserir médias
        tree.insert("", "end", values=("Idade", f"{media_idade:.2f}"))
        tree.insert("", "end", values=("Peso", f"{media_peso:.2f}"))


    def gerenciar_usuarios(self):
        nova_janela = tk.Toplevel(self.root)
        UsuariosUI(nova_janela)
