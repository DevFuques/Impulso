import tkinter as tk
from tkinter import ttk, messagebox
from models.usuarios import cadastrar_usuario, listar_usuarios, deletar_usuario, atualizar_usuario

class UsuariosUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciar Usuários")
        self.root.geometry("600x550")

        frame = ttk.Frame(self.root, padding=10)
        frame.pack(expand=True, fill="both")

        # --- Campos de cadastro / edição ---
        ttk.Label(frame, text="Usuário:").pack(anchor="w")
        self.entry_usuario = ttk.Entry(frame, width=30)
        self.entry_usuario.pack(pady=5)

        ttk.Label(frame, text="Senha:").pack(anchor="w")
        self.entry_senha = ttk.Entry(frame, width=30, show="*")
        self.entry_senha.pack(pady=5)

        ttk.Label(frame, text="Tipo:").pack(anchor="w")
        self.entry_tipo = ttk.Combobox(frame, values=["usuario", "admin"], width=28)
        self.entry_tipo.current(0)
        self.entry_tipo.pack(pady=5)

        # Botão salvar/atualizar
        self.btn_salvar = ttk.Button(frame, text="Salvar Usuário", command=self.salvar_usuario)
        self.btn_salvar.pack(pady=10)

        # --- Treeview para exibir usuários ---
        colunas = ("id", "usuario", "tipo")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings")
        for col in colunas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150)
        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<Double-1>", self.carregar_para_editar)  # duplo clique para editar

        # --- Botões Atualizar e Deletar ---
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="🔄 Atualizar", command=self.carregar_dados).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑 Deletar Selecionado", command=self.deletar_selecionado).pack(side="left", padx=5)

        self.carregar_dados()

    # --- Funções ---
    def salvar_usuario(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        tipo = self.entry_tipo.get()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        # Verifica se estamos editando ou criando novo
        if hasattr(self, "usuario_editando_id"):
            atualizar_usuario(self.usuario_editando_id, usuario, senha, tipo)
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            del self.usuario_editando_id
            self.btn_salvar.config(text="Salvar Usuário")
        else:
            cadastrar_usuario(usuario, senha, tipo)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

        self.limpar_campos()
        self.carregar_dados()

    def carregar_dados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        usuarios = listar_usuarios()
        for u in usuarios:
            self.tree.insert("", "end", values=u)

    def deletar_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um usuário para deletar!")
            return

        item = self.tree.item(selecionado)
        usuario_id = item["values"][0]

        confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este usuário?")
        if confirmar:
            deletar_usuario(usuario_id)
            messagebox.showinfo("Sucesso", "Usuário deletado com sucesso!")
            self.carregar_dados()

    def carregar_para_editar(self, event):
        selecionado = self.tree.selection()
        if not selecionado:
            return

        item = self.tree.item(selecionado)
        usuario_id, usuario, tipo = item["values"]

        self.usuario_editando_id = usuario_id
        self.entry_usuario.delete(0, tk.END)
        self.entry_usuario.insert(0, usuario)
        self.entry_senha.delete(0, tk.END)
        self.entry_tipo.set(tipo)
        self.btn_salvar.config(text="Atualizar Usuário")

    def limpar_campos(self):
        self.entry_usuario.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.entry_tipo.current(0)
