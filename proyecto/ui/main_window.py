import tkinter as tk
from tkinter import ttk
from ui.login_window import LoginWindow
from ui.signup_window import SignUpWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Bienvenido a Comparador App")
        self.root.geometry("500x500")
        self.root.configure(bg="#f4f4f4")

        tk.Label(root, text="Comparador de Supermercados", font=("Helvetica", 18, "bold"), bg="#f4f4f4").pack(pady=30)

        ttk.Button(root, text="Log In", command=self.open_login).pack(pady=10)
        ttk.Button(root, text="Sign Up", command=self.open_signup).pack(pady=10)
        tk.Button(root, text="Salir", command=root.destroy).pack(pady=10)

    def open_login(self):
        LoginWindow(self.root)

    def open_signup(self):
        SignUpWindow(self.root)
