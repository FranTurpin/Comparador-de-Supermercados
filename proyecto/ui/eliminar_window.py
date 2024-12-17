import tkinter as tk
from tkinter import messagebox
import asyncio
from db.db_operations import fetch_data, execute_query

class EliminarWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Eliminar Producto")
        self.window.geometry("400x300")
        self.window.configure(bg="#f4f4f4")

        tk.Label(self.window, text="Selecciona un producto a eliminar:", font=("Helvetica", 12), bg="#f4f4f4").pack(pady=10)

        # Variable para almacenar productos
        self.productos = []  # Lista de productos para el OptionMenu
        self.selected_producto = tk.StringVar(self.window)  # Producto seleccionado

        # Cargar productos desde la base de datos
        asyncio.run(self.cargar_productos())

        # Menú desplegable
        self.dropdown = tk.OptionMenu(self.window, self.selected_producto, *self.productos)
        self.dropdown.pack(pady=10)

        # Botón para eliminar producto
        tk.Button(self.window, text="Eliminar Producto", command=self.eliminar_producto).pack(pady=20)

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

            if self.productos:
                self.selected_producto.set(self.productos[0])  # Valor inicial
            else:
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
