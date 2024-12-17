import customtkinter as ctk
from tkinter import messagebox
from db.db_operations import add_supermercado

class AddSupermercadoWindow:
    def __init__(self, root):
        self.window = ctk.CTkToplevel(root)
        self.window.title("Añadir Supermercado")
        self.window.geometry("400x200")
        self.window.resizable(False, False)

        # Configurar estilo oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame principal con fondo oscuro
        main_frame = ctk.CTkFrame(self.window, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título principal
        title_label = ctk.CTkLabel(main_frame, text="Añadir Supermercado",
                                   font=("Helvetica", 18, "bold"), text_color="white")
        title_label.pack(pady=10)

        # Etiqueta y entrada para el nombre del supermercado
        name_label = ctk.CTkLabel(main_frame, text="Nombre del supermercado:", font=("Helvetica", 14), text_color="white")
        name_label.pack(pady=(10, 5))

        self.supermercado_entry = ctk.CTkEntry(main_frame, placeholder_text="Escribe el nombre aquí", width=250)
        self.supermercado_entry.pack(pady=5)

        # Botón para añadir supermercado
        add_button = ctk.CTkButton(main_frame, text="Añadir", command=self.add_supermercado, width=150)
        add_button.pack(pady=20)

    def add_supermercado(self):
        """
        Añade un supermercado a la base de datos.
        """
        nombre = self.supermercado_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre del supermercado no puede estar vacío.")
            return

        if add_supermercado(nombre):
            messagebox.showinfo("Éxito", f"¡Supermercado '{nombre}' añadido correctamente!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo añadir el supermercado.")
