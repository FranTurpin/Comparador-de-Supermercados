import customtkinter as ctk
from tkinter import messagebox
from db.db_operations import eliminar_supermercado, obtener_supermercados

class EliminarSupermercadoWindow:
    def __init__(self, root):
        self.window = ctk.CTkToplevel(root)
        self.window.title("Eliminar Supermercado")
        self.window.geometry("400x200")
        self.window.resizable(False, False)

        # Configurar el estilo oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame principal con fondo oscuro
        main_frame = ctk.CTkFrame(self.window, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título principal
        title_label = ctk.CTkLabel(main_frame, text="Eliminar Supermercado",
                                   font=("Helvetica", 18, "bold"), text_color="white")
        title_label.pack(pady=10)

        # Subtítulo
        subtitle_label = ctk.CTkLabel(main_frame, text="Selecciona un supermercado a eliminar:",
                                      font=("Helvetica", 14), text_color="white")
        subtitle_label.pack(pady=10)

        # Desplegable de supermercados
        self.supermercados = self.cargar_supermercados()
        self.selected_supermercado = ctk.StringVar(value=self.supermercados[0] if self.supermercados else "No hay supermercados")

        self.dropdown = ctk.CTkOptionMenu(main_frame, variable=self.selected_supermercado,
                                          values=self.supermercados if self.supermercados else ["No hay supermercados"])
        self.dropdown.pack(pady=10)

        # Botón Eliminar
        delete_button = ctk.CTkButton(main_frame, text="Eliminar", command=self.eliminar_supermercado, width=150)
        delete_button.pack(pady=10)

    def cargar_supermercados(self):
        """
        Cargar la lista de supermercados desde la base de datos.
        """
        try:
            result = obtener_supermercados()
            if result:
                return [supermercado['nombre'] for supermercado in result]
            else:
                messagebox.showerror("Error", "No hay supermercados disponibles en la base de datos.")
                return []
        except Exception as e:
            print(f"Error al cargar supermercados: {e}")
            messagebox.showerror("Error", "Ocurrió un error al cargar los supermercados.")
            return []

    def eliminar_supermercado(self):
        """
        Elimina el supermercado seleccionado de la base de datos.
        """
        nombre = self.selected_supermercado.get()
        if not nombre or nombre == "No hay supermercados":
            messagebox.showerror("Error", "Selecciona un supermercado válido.")
            return

        try:
            if eliminar_supermercado(nombre):
                messagebox.showinfo("Éxito", f"¡Supermercado '{nombre}' eliminado correctamente!")
                self.window.destroy()
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el supermercado '{nombre}'.")
        except Exception as e:
            print(f"Error al eliminar supermercado: {e}")
            messagebox.showerror("Error", "Ocurrió un error al eliminar el supermercado.")
