import tkinter as tk
from db import inicializa_banco
from config import configurar_tema
from ui.login import LoginApp
from models.usuarios import inicializa_admin

def main():
    inicializa_banco()
    inicializa_admin()
    root = tk.Tk()
    configurar_tema(root)
    LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
