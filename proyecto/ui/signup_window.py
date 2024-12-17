import tkinter as tk
from tkinter import messagebox
from db.db_operations import execute_query

class SignUpWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Sign Up")
        self.window.geometry("400x400")

        tk.Label(self.window, text="Usuario:").pack(pady=10)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        tk.Label(self.window, text="Email:").pack(pady=10)
        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack()

        tk.Label(self.window, text="Contraseña:").pack(pady=10)
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        tk.Button(self.window, text="Registrar", command=self.sign_up).pack(pady=20)

    def sign_up(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        query = "INSERT INTO usuarios (username, email, password) VALUES ($1, $2, $3)"
        if asyncio.run(execute_query(query, username, email, password)):
            messagebox.showinfo("Sign Up", "Registro exitoso")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Error al registrar usuario")
