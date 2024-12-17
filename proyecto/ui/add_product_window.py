import tkinter as tk
from tkinter import messagebox
import asyncio
from db.db_operations import fetch_data, execute_query  # Funciones de base de datos

class AddProductWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Añadir Producto")
        self.window.geometry("400x300")
        self.window.configure(bg="#f4f4f4")

        # Etiquetas y campos de entrada
        tk.Label(self.window, text="Nombre del Producto:", font=("Helvetica", 12), bg="#f4f4f4").pack(pady=5)
        self.producto_entry = tk.Entry(self.window, font=("Helvetica", 12))
        self.producto_entry.pack(pady=5)

        tk.Label(self.window, text="Precio:", font=("Helvetica", 12), bg="#f4f4f4").pack(pady=5)
        self.precio_entry = tk.Entry(self.window, font=("Helvetica", 12))
        self.precio_entry.pack(pady=5)

        tk.Label(self.window, text="Selecciona un Supermercado:", font=("Helvetica", 12), bg="#f4f4f4").pack(pady=5)

        # Desplegable de supermercados
        self.supermercados = []
        self.selected_supermercado = tk.StringVar(self.window)
        self.selected_supermercado.set("Cargando...")  # Placeholder inicial

        self.dropdown = tk.OptionMenu(self.window, self.selected_supermercado, ())
        self.dropdown.pack(pady=5)

        # Botón para añadir producto
        tk.Button(self.window, text="Añadir Producto", width=20, command=self.add_product).pack(pady=20)

        # Cargar supermercados al iniciar
        asyncio.run(self.cargar_supermercados())

    async def cargar_supermercados(self):
        """
        Cargar la lista de supermercados desde la base de datos y actualizar el desplegable.
        """
        query = "SELECT id, nombre FROM supermercados"
        try:
            result = await fetch_data(query)
            if not result:
                messagebox.showerror("Error", "No hay supermercados disponibles en la base de datos.")
                self.selected_supermercado.set("No hay supermercados")
                return

            # Guardar supermercados y actualizar el OptionMenu
            self.supermercados = {row["nombre"]: row["id"] for row in result}
            menu = self.dropdown["menu"]
            menu.delete(0, "end")  # Eliminar opciones anteriores

            for nombre in self.supermercados.keys():
                menu.add_command(label=nombre, command=lambda value=nombre: self.selected_supermercado.set(value))

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
        if not producto or not precio or not supermercado_nombre:
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
