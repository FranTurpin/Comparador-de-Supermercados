import customtkinter as ctk
from tkinter import messagebox
import asyncio
from db.db_operations import fetch_data, execute_query

class EliminarWindow:
    def __init__(self, root):
        self.window = ctk.CTkToplevel(root)
        self.window.title("Eliminar Producto")
        self.window.geometry("400x300")
        self.window.resizable(False, False)

        # Configurar estilo oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame principal con fondo oscuro
        main_frame = ctk.CTkFrame(self.window, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Etiqueta de título
        title_label = ctk.CTkLabel(main_frame, text="Eliminar Producto",
                                   font=("Helvetica", 20, "bold"), text_color="white")
        title_label.pack(pady=20)

        # Subtítulo
        subtitle_label = ctk.CTkLabel(main_frame, text="Selecciona un producto a eliminar:",
                                      font=("Helvetica", 14), text_color="white")
        subtitle_label.pack(pady=10)

        # Variable para almacenar productos
        self.productos = []  # Lista de productos para el OptionMenu
        self.selected_producto = ctk.StringVar(value="Cargando productos...")

        # Menú desplegable
        self.dropdown = ctk.CTkOptionMenu(main_frame, variable=self.selected_producto, values=["Cargando..."])
        self.dropdown.pack(pady=10)

        # Botón para eliminar producto
        delete_button = ctk.CTkButton(main_frame, text="Eliminar Producto", command=self.eliminar_producto, width=150)
        delete_button.pack(pady=20)

        # Cargar productos desde la base de datos
        asyncio.run(self.cargar_productos())

        # Mensaje si no hay productos
        if not self.productos:
            self.selected_producto.set("No hay productos disponibles")

    async def cargar_productos(self):
        """
        Carga los nombres de productos junto con sus supermercados desde la base de datos.
        """
        query = """
        SELECT p.nombre AS producto, s.nombre AS supermercado
        FROM productos p
        JOIN supermercados s ON p.supermercados_id = s.id
        """
        try:
            result = await fetch_data(query)
            # Combina el producto y el supermercado entre paréntesis
            self.productos = [f"{row['producto']} ({row['supermercado']})" for row in result]

            # Actualizar el OptionMenu si hay productos
            if self.productos:
                self.dropdown.configure(values=self.productos)
                self.selected_producto.set(self.productos[0])  # Selección inicial
            else:
                self.dropdown.configure(values=["No hay productos disponibles"])
                self.selected_producto.set("No hay productos disponibles")
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            messagebox.showerror("Error", "Error al cargar productos.")

    def eliminar_producto(self):
        """
        Elimina el producto seleccionado de la base de datos.
        """
        producto_seleccionado = self.selected_producto.get()

        if not producto_seleccionado or producto_seleccionado == "No hay productos disponibles":
            messagebox.showerror("Error", "Por favor selecciona un producto válido.")
            return

        # Extraer el nombre del producto eliminando el supermercado entre paréntesis
        producto = producto_seleccionado.split(" (")[0]

        query = "DELETE FROM productos WHERE nombre = $1"
        try:
            if asyncio.run(execute_query(query, producto)):
                messagebox.showinfo("Éxito", f"Producto '{producto}' eliminado correctamente.")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto.")
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            messagebox.showerror("Error", "Error al eliminar el producto.")
