import customtkinter as ctk
from tkinter import messagebox
import asyncio
from db.db_operations import fetch_data

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.window = ctk.CTkToplevel(root)
        self.window.title("Log In")
        self.window.geometry("500x400")
        self.window.resizable(False, False)

        # Configurar estilo oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame principal
        main_frame = ctk.CTkFrame(self.window, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Etiqueta de título
        title_label = ctk.CTkLabel(main_frame, text="Iniciar Sesión", font=("Helvetica", 20, "bold"), text_color="white")
        title_label.pack(pady=20)

        # Campos de usuario y contraseña
        ctk.CTkLabel(main_frame, text="Usuario:", font=("Helvetica", 14), text_color="white").pack(pady=(5, 0))
        self.username_entry = ctk.CTkEntry(main_frame, placeholder_text="Escribe tu usuario", width=250)
        self.username_entry.pack(pady=5)

        ctk.CTkLabel(main_frame, text="Contraseña:", font=("Helvetica", 14), text_color="white").pack(pady=(5, 0))
        self.password_entry = ctk.CTkEntry(main_frame, placeholder_text="Escribe tu contraseña", show="*", width=250)
        self.password_entry.pack(pady=5)

        # Botón Iniciar Sesión
        login_button = ctk.CTkButton(main_frame, text="Iniciar Sesión", command=self.log_in, width=200)
        login_button.pack(pady=20)

    def log_in(self):
        """Verifica las credenciales y abre la ventana principal."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return

        query = "SELECT * FROM usuarios WHERE username = $1 AND password = $2"
        try:
            result = asyncio.run(fetch_data(query, username, password))
            if result:
                from ui.main_menu_window import MainMenuWindow  # Importación local para evitar ciclo
                self.root.withdraw()  # Oculta la ventana principal
                self.window.destroy()  # Cierra la ventana de login
                MainMenuWindow(self.root, username)  # Abre el menú principal
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            messagebox.showerror("Error", "Ocurrió un error al iniciar sesión.")
