import customtkinter as ctk
from tkinter import messagebox
import asyncio
from db.db_operations import execute_query

class SignUpWindow:
    def __init__(self, root):
        self.window = ctk.CTkToplevel(root)  # Crear ventana secundaria
        self.window.title("Sign Up")
        self.window.geometry("400x400")
        self.window.resizable(False, False)

        # Configuración del estilo
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame principal
        main_frame = ctk.CTkFrame(self.window, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Etiqueta de título
        title_label = ctk.CTkLabel(main_frame, text="Registro de Usuario",
                                   font=("Helvetica", 20, "bold"), text_color="white")
        title_label.pack(pady=20)

        # Campo de entrada para Usuario
        username_label = ctk.CTkLabel(main_frame, text="Usuario:", font=("Helvetica", 14))
        username_label.pack(pady=(10, 5))
        self.username_entry = ctk.CTkEntry(main_frame, placeholder_text="Escribe tu usuario", width=250)
        self.username_entry.pack(pady=(0, 10))

        # Campo de entrada para Email
        email_label = ctk.CTkLabel(main_frame, text="Email:", font=("Helvetica", 14))
        email_label.pack(pady=(10, 5))
        self.email_entry = ctk.CTkEntry(main_frame, placeholder_text="Escribe tu email", width=250)
        self.email_entry.pack(pady=(0, 10))

        # Campo de entrada para Contraseña
        password_label = ctk.CTkLabel(main_frame, text="Contraseña:", font=("Helvetica", 14))
        password_label.pack(pady=(10, 5))
        self.password_entry = ctk.CTkEntry(main_frame, placeholder_text="Escribe tu contraseña", show="*", width=250)
        self.password_entry.pack(pady=(0, 20))

        # Botón para Registrar
        register_button = ctk.CTkButton(main_frame, text="Registrar", command=self.sign_up, width=150, height=35)
        register_button.pack(pady=10)

        # Hacer la ventana modal
        self.window.grab_set()

    def sign_up(self):
        """
        Realiza el registro del usuario en la base de datos.
        """
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not username or not email or not password:
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return

        query = "INSERT INTO usuarios (username, email, password) VALUES ($1, $2, $3)"
        try:
            if asyncio.run(execute_query(query, username, email, password)):
                messagebox.showinfo("Sign Up", "Registro exitoso")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Error al registrar usuario")
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            messagebox.showerror("Error", "Ocurrió un error al registrar el usuario")

