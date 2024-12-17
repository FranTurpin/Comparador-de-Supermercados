import tkinter as tk
from tkinter import messagebox
import asyncio
from db.db_operations import fetch_data
from ui.main_menu_window import MainMenuWindow  # Importar la ventana del menú principal

class LoginWindow:
    def __init__(self, root):
        self.root = root  # Referencia a la ventana principal
        self.window = tk.Toplevel(root)
        self.window.title("Log In")
        self.window.geometry("400x300")
        self.window.configure(bg="#f4f4f4")

        tk.Label(self.window, text="Usuario:", font=("Helvetica", 12), bg="#f4f4f4").pack(pady=10)
        self.username_entry = tk.Entry(self.window, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.window, text="Contraseña:", font=("Helvetica", 12), bg="#f4f4f4").pack(pady=10)
        self.password_entry = tk.Entry(self.window, font=("Helvetica", 12), show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.window, text="Iniciar Sesión", command=self.log_in).pack(pady=20)

    def log_in(self):
        """
        Verifica las credenciales del usuario y abre la ventana principal si son correctas.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return

        query = "SELECT * FROM usuarios WHERE username = $1 AND password = $2"
        try:
            # Ejecutar consulta SQL
            result = asyncio.run(fetch_data(query, username, password))

            # Si el login es exitoso
            if result:
                self.root.withdraw()  # Oculta la ventana principal (MainWindow)
                self.window.destroy()  # Cierra la ventana de Login
                MainMenuWindow(self.root, username)  # Abre el menú principal como un Toplevel
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        except Exception as e:
            print(f"Error al realizar la consulta SQL: {e}")
            messagebox.showerror("Error", "Ocurrió un error al iniciar sesión.")
