import tkinter as tk
from tkinter import ttk, messagebox
from models.usuarios import login
from ui.menu import MenuPrincipal

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Impulso - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="🔐 Login", style="Header.TLabel").pack(pady=15)

        ttk.Label(frame, text="👤 Usuário:").pack(anchor="w")
        self.entry_usuario = ttk.Entry(frame, width=30)
        self.entry_usuario.pack(pady=5)

        ttk.Label(frame, text="🔒 Senha:").pack(anchor="w")
        self.entry_senha = ttk.Entry(frame, width=30, show="*")
        self.entry_senha.pack(pady=5)

        ttk.Button(frame, text="Entrar", command=self.fazer_login).pack(pady=15)

    def fazer_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        resultado = login(usuario, senha)

        if resultado:
            nome, tipo = resultado
            messagebox.showinfo("Sucesso", f"Bem-vindo, {nome}! ({tipo})")
            self.root.destroy()
            nova_janela = tk.Tk()
            from config import configurar_tema
            configurar_tema(nova_janela)
            MenuPrincipal(nova_janela, tipo)
            nova_janela.mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")
