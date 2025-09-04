import tkinter as tk
from tkinter import ttk, messagebox
from models.pessoas import cadastrar_pessoa, listar_pessoas, deletar_pessoa, buscar_endereco_por_cep

class CadastroPessoaUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Pessoa")
        self.root.geometry("400x620")

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")

        # Nome
        ttk.Label(frame, text="Nome:").pack(anchor="w")
        self.entry_nome = ttk.Entry(frame, width=40)
        self.entry_nome.pack(pady=5)

        # Idade
        ttk.Label(frame, text="Idade:").pack(anchor="w")
        self.entry_idade = ttk.Entry(frame, width=10)
        self.entry_idade.pack(pady=5)

        # Peso
        ttk.Label(frame, text="Peso:").pack(anchor="w")
        self.entry_peso = ttk.Entry(frame, width=10)
        self.entry_peso.pack(pady=5)

        # CEP
        ttk.Label(frame, text="CEP:").pack(anchor="w")
        self.entry_cep = ttk.Entry(frame, width=15)
        self.entry_cep.pack(pady=5)

        ttk.Button(frame, text="Buscar Endereço", command=self.preencher_endereco).pack(pady=5)

        # Campos de endereço
        self.entry_logradouro = ttk.Entry(frame, width=40)
        self.entry_bairro = ttk.Entry(frame, width=40)
        self.entry_cidade = ttk.Entry(frame, width=40)
        self.entry_estado = ttk.Entry(frame, width=5)

        ttk.Label(frame, text="Logradouro:").pack(anchor="w")
        self.entry_logradouro.pack(pady=5)
        ttk.Label(frame, text="Bairro:").pack(anchor="w")
        self.entry_bairro.pack(pady=5)
        ttk.Label(frame, text="Cidade:").pack(anchor="w")
        self.entry_cidade.pack(pady=5)
        ttk.Label(frame, text="Estado:").pack(anchor="w")
        self.entry_estado.pack(pady=5)

        ttk.Button(frame, text="Salvar", command=self.salvar).pack(pady=15)

    def preencher_endereco(self):
        cep = self.entry_cep.get().strip()
        if cep:
            endereco = buscar_endereco_por_cep(cep)
            if endereco:
                self.entry_logradouro.delete(0, tk.END)
                self.entry_logradouro.insert(0, endereco["logradouro"])
                self.entry_bairro.delete(0, tk.END)
                self.entry_bairro.insert(0, endereco["bairro"])
                self.entry_cidade.delete(0, tk.END)
                self.entry_cidade.insert(0, endereco["cidade"])
                self.entry_estado.delete(0, tk.END)
                self.entry_estado.insert(0, endereco["estado"])
            else:
                messagebox.showerror("Erro", "CEP inválido ou não encontrado!")
        else:
            messagebox.showwarning("Aviso", "Digite um CEP!")

    def salvar(self):
        nome = self.entry_nome.get().strip()
        idade = self.entry_idade.get().strip()
        peso = self.entry_peso.get().strip()
        cep = self.entry_cep.get().strip()
        logradouro = self.entry_logradouro.get().strip()
        bairro = self.entry_bairro.get().strip()
        cidade = self.entry_cidade.get().strip()
        estado = self.entry_estado.get().strip()

        if not (nome and idade and peso):
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios!")
            return

        cadastrar_pessoa(nome, int(idade), float(peso), cep, logradouro, bairro, cidade, estado)
        messagebox.showinfo("Sucesso", "Pessoa cadastrada com sucesso!")
        self.root.destroy()

class ExibirPessoasUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Pessoas")
        self.root.geometry("900x400")

        frame = ttk.Frame(self.root, padding=10)
        frame.pack(expand=True, fill="both")

        # Criando a tabela
        colunas = ("id", "nome", "idade", "peso", "cep", "logradouro", "bairro", "cidade", "estado")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings")

        # Cabeçalhos
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("idade", text="Idade")
        self.tree.heading("peso", text="Peso")
        self.tree.heading("cep", text="CEP")
        self.tree.heading("logradouro", text="Logradouro")
        self.tree.heading("bairro", text="Bairro")
        self.tree.heading("cidade", text="Cidade")
        self.tree.heading("estado", text="Estado")

        # Ajuste de largura
        self.tree.column("id", width=40)
        self.tree.column("nome", width=120)
        self.tree.column("idade", width=60)
        self.tree.column("peso", width=60)
        self.tree.column("cep", width=100)
        self.tree.column("logradouro", width=150)
        self.tree.column("bairro", width=120)
        self.tree.column("cidade", width=120)
        self.tree.column("estado", width=60)

        self.tree.pack(expand=True, fill="both")

        # Botão atualizar
        ttk.Button(frame, text="🔄 Atualizar", command=self.carregar_dados).pack(pady=10)
        ttk.Button(frame, text="🗑️ Deletar Selecionado", command=self.deletar_selecionado).pack(pady=5)
        self.carregar_dados()

    def carregar_dados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        pessoas = listar_pessoas()
        if pessoas:
            for pessoa in pessoas:
                self.tree.insert("", "end", values=pessoa)
        else:
            messagebox.showinfo("Info", "Nenhuma pessoa cadastrada.")
    
    def deletar_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma pessoa para deletar!")
            return

        item = self.tree.item(selecionado)
        pessoa_id = item["values"][0]  # ID da pessoa na primeira coluna
        
        confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar esta pessoa?")
        if confirmar:
            deletar_pessoa(pessoa_id)
            messagebox.showinfo("Sucesso", "Pessoa deletada com sucesso!")
            self.carregar_dados()