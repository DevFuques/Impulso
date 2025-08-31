from tkinter import ttk

def configurar_tema(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    root.configure(bg="#1e1e1e")

    style.configure("TFrame", background="#1e1e1e")
    style.configure("TLabel", background="#1e1e1e", foreground="#f1f1f1", font=("Segoe UI", 11))
    style.configure("Header.TLabel", background="#1e1e1e", foreground="#ffcc00", font=("Segoe UI", 16, "bold"))

    style.configure("TButton",
                    background="#ffcc00", foreground="#000000",
                    font=("Segoe UI", 11, "bold"), padding=6)

    style.map("TButton",
              background=[("active", "#e6b800")],
              foreground=[("active", "#000000")])

    style.configure("TEntry",
                    fieldbackground="#2d2d2d", foreground="#ffffff",
                    insertcolor="#ffcc00")
