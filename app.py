import tkinter as tk
from db import inicializa_banco
from config import configurar_tema
from ui.login import LoginApp

def main():
    inicializa_banco()
    root = tk.Tk()
    configurar_tema(root)
    LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
