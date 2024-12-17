import customtkinter as ctk
from tkinter import messagebox
import asyncio
from db.db_operations import fetch_data, execute_query  # Funciones de base de datos

class AddProductWindow:
    def __init__(self, root):
        self.window = ctk.CTkToplevel(root)
        self.window.title("Añadir Producto")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        # Configuración del estilo oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame principal con fondo oscuro
        main_frame = ctk.CTkFrame(self.window, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título principal
        title_label = ctk.CTkLabel(main_frame, text="Añadir Producto",
                                   font=("Helvetica", 18, "bold"), text_color="white")
        title_label.pack(pady=10)

        # Entrada para nombre del producto
        name_label = ctk.CTkLabel(main_frame, text="Nombre del Producto:", font=("Helvetica", 14), text_color="white")
        name_label.pack(pady=(10, 5))
        self.producto_entry = ctk.CTkEntry(main_frame, placeholder_text="Escribe el nombre del producto", width=250)
        self.producto_entry.pack(pady=(0, 10))

        # Entrada para precio
        price_label = ctk.CTkLabel(main_frame, text="Precio:", font=("Helvetica", 14), text_color="white")
        price_label.pack(pady=(10, 5))
        self.precio_entry = ctk.CTkEntry(main_frame, placeholder_text="Escribe el precio", width=250)
        self.precio_entry.pack(pady=(0, 10))

        # Menú desplegable para supermercados
        supermercado_label = ctk.CTkLabel(main_frame, text="Selecciona un Supermercado:", font=("Helvetica", 14), text_color="white")
        supermercado_label.pack(pady=(10, 5))

        self.supermercados = {}
        self.selected_supermercado = ctk.StringVar(value="Cargando...")
        self.dropdown = ctk.CTkOptionMenu(main_frame, variable=self.selected_supermercado, values=["Cargando..."])
        self.dropdown.pack(pady=(0, 20))

        # Botón para añadir producto
        add_button = ctk.CTkButton(main_frame, text="Añadir Producto", command=self.add_product, width=150)
        add_button.pack(pady=10)

        # Cargar supermercados
        asyncio.run(self.cargar_supermercados())

    async def cargar_supermercados(self):
        """
        Cargar la lista de supermercados desde la base de datos y actualizar el menú desplegable.
        """
        query = "SELECT id, nombre FROM supermercados"
        try:
            result = await fetch_data(query)
            if not result:
                messagebox.showerror("Error", "No hay supermercados disponibles en la base de datos.")
                self.dropdown.configure(values=["No hay supermercados"])
                self.selected_supermercado.set("No hay supermercados")
                return

            # Guardar supermercados y actualizar el OptionMenu
            self.supermercados = {row["nombre"]: row["id"] for row in result}
            self.dropdown.configure(values=list(self.supermercados.keys()))
            self.selected_supermercado.set(next(iter(self.supermercados)))  # Seleccionar el primer supermercado
        except Exception as e:
            print(f"Error al cargar supermercados: {e}")
            messagebox.showerror("Error", "Ocurrió un error al cargar supermercados.")

    def add_product(self):
        """
        Añadir el producto a la base de datos con el supermercado seleccionado.
        """
        producto = self.producto_entry.get().strip()
        precio = self.precio_entry.get().strip()
        supermercado_nombre = self.selected_supermercado.get()

        # Validaciones
        if not producto or not precio or supermercado_nombre == "No hay supermercados":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not precio.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        supermercado_id = self.supermercados[supermercado_nombre]
        query = """
        INSERT INTO productos (nombre, precio, supermercados_id)
        VALUES ($1, $2, $3)
        """
        try:
            if asyncio.run(execute_query(query, producto, float(precio), supermercado_id)):
                messagebox.showinfo("Éxito", f"Producto '{producto}' añadido al supermercado '{supermercado_nombre}'.")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo añadir el producto.")
        except Exception as e:
            print(f"Error al añadir producto: {e}")
            messagebox.showerror("Error", "Ocurrió un error al añadir el producto.")
