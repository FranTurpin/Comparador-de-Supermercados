import tkinter as tk
from tkinter import messagebox
from db.db_operations import obtener_precios_productos_por_supermercado

class ListaWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Crear lista de la compra")
        self.window.geometry("500x500")
        self.window.configure(bg="#fafafa")

        # Título principal
        tk.Label(self.window, text="Lista de la Compra", font=("Helvetica", 14, "bold"), bg="#fafafa").pack(pady=10)

        # Frame para la lista seleccionada
        self.lista_frame = tk.Frame(self.window, bg="#fafafa")
        self.lista_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Frame para añadir productos
        self.add_frame = tk.Frame(self.window, bg="#fafafa")
        self.add_frame.pack(pady=10)

        # Widgets para añadir productos
        self.productos_dict = {}
        self.selected_producto = tk.StringVar(self.window)
        self.selected_producto.set("Selecciona un producto")

        self.cantidad_entry = tk.Entry(self.add_frame, width=5)
        tk.Label(self.add_frame, text="Cantidad:", bg="#fafafa").pack(side=tk.LEFT, padx=5)
        self.cantidad_entry.pack(side=tk.LEFT, padx=5)

        self.dropdown = tk.OptionMenu(self.add_frame, self.selected_producto, "Cargando...")
        self.dropdown.pack(side=tk.LEFT, padx=5)

        tk.Button(self.add_frame, text="Añadir", command=self.añadir_a_lista).pack(side=tk.LEFT, padx=5)

        # Lista de productos seleccionados
        self.lista_productos = []

        # Botón para calcular el precio
        tk.Button(self.window, text="Calcular Precio", command=self.calcular_precio).pack(pady=10)

        self.cargar_productos()

    def cargar_productos(self):
        """
        Cargar los productos desde la base de datos y actualizar el desplegable.
        """
        precios = obtener_precios_productos_por_supermercado()
        if not precios:
            messagebox.showerror("Error", "No se pudo cargar la lista de productos.")
            return

        # Obtener la lista única de productos
        productos_unicos = set()
        for productos_super in precios.values():
            productos_unicos.update(productos_super.keys())

        self.productos_dict = list(productos_unicos)

        # Actualizar el OptionMenu
        menu = self.dropdown["menu"]
        menu.delete(0, "end")
        for producto in self.productos_dict:
            menu.add_command(label=producto, command=lambda p=producto: self.selected_producto.set(p))
        self.selected_producto.set(self.productos_dict[0] if self.productos_dict else "No hay productos disponibles")

    def añadir_a_lista(self):
        """
        Añadir el producto seleccionado y su cantidad a la lista.
        """
        producto = self.selected_producto.get()
        cantidad = self.cantidad_entry.get()

        if producto == "No hay productos disponibles" or not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Selecciona un producto válido y cantidad mayor que 0.")
            return

        # Añadir a la lista de productos seleccionados
        cantidad = int(cantidad)
        self.lista_productos.append((producto, cantidad))

        # Mostrar en la interfaz
        tk.Label(self.lista_frame, text=f"{producto} x{cantidad}", bg="#fafafa").pack()

        # Limpiar la cantidad
        self.cantidad_entry.delete(0, tk.END)

    def calcular_precio(self):
        """
        Calcular el precio total de la lista seleccionada en cada supermercado.
        Mostrar los productos faltantes y el supermercado más barato que tenga todos los productos.
        """
        if not self.lista_productos:
            messagebox.showinfo("Precio", "La lista está vacía. Añade productos primero.")
            return

        # Obtener precios de productos por supermercado
        precios = obtener_precios_productos_por_supermercado()

        # Calcular precios por supermercado y productos faltantes
        precios_totales = {}
        productos_faltantes = {}

        for producto, cantidad in self.lista_productos:
            for supermercado, productos in precios.items():
                if supermercado not in precios_totales:
                    precios_totales[supermercado] = 0
                    productos_faltantes[supermercado] = []

                precio_producto = productos.get(producto)
                if precio_producto is not None:
                    precios_totales[supermercado] += precio_producto * cantidad
                else:
                    productos_faltantes[supermercado].append(producto)

        # Filtrar supermercados que tienen todos los productos
        supermercados_validos = {super: total for super, total in precios_totales.items() 
                                 if not productos_faltantes[super]}

        # Determinar el supermercado más barato (que tenga todos los productos)
        if supermercados_validos:
            supermercado_mas_barato = min(supermercados_validos, key=supermercados_validos.get)
            total_mas_barato = supermercados_validos[supermercado_mas_barato]
        else:
            supermercado_mas_barato = None

        # Mostrar resultados
        resultado = ""
        for supermercado, total in precios_totales.items():
            faltantes = ", ".join(productos_faltantes[supermercado])
            resultado += f"{supermercado}: {total:.2f}€"
            if faltantes:
                resultado += f" (Sin: {faltantes})"
            resultado += "\n"

        if supermercado_mas_barato:
            resultado += f"\nEl supermercado más barato es '{supermercado_mas_barato}' con un total de {total_mas_barato:.2f}€."
        else:
            resultado += "\nNo hay ningún supermercado que disponga de todos los productos."

        messagebox.showinfo("Precios por Supermercado", resultado)
