import customtkinter as ctk
from tkinter import messagebox, simpledialog
from db.db_operations import obtener_precios_productos_por_supermercado

class ListaWindow:
    def __init__(self, root):
        self.window = ctk.CTkToplevel(root)
        self.window.title("Crear lista de la compra")
        self.window.geometry("500x500")
        self.window.resizable(False, False)

        # Configurar estilo oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame principal
        main_frame = ctk.CTkFrame(self.window, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título principal
        title_label = ctk.CTkLabel(main_frame, text="Lista de la Compra", font=("Helvetica", 18, "bold"), text_color="white")
        title_label.pack(pady=10)

        # Frame para la lista seleccionada
        self.lista_frame = ctk.CTkFrame(main_frame, fg_color="#3b3b3b", corner_radius=10)
        self.lista_frame.pack(fill="both", expand=True, pady=10)

        # Frame para añadir productos
        self.add_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b", corner_radius=10)
        self.add_frame.pack(pady=10)

        # Widgets para añadir productos
        self.productos_dict = {}
        self.selected_producto = ctk.StringVar(value="Selecciona un producto")

        ctk.CTkLabel(self.add_frame, text="Cantidad:", font=("Helvetica", 14), text_color="white").pack(side="left", padx=5)

        # Botones +, -, y campo cantidad
        self.cantidad_var = ctk.StringVar(value="1")
        self.decrementar_btn = ctk.CTkButton(self.add_frame, text="-", width=30, command=self.decrementar_cantidad)
        self.decrementar_btn.pack(side="left", padx=5)
        self.cantidad_entry = ctk.CTkEntry(self.add_frame, width=50, textvariable=self.cantidad_var)
        self.cantidad_entry.pack(side="left", padx=5)
        self.incrementar_btn = ctk.CTkButton(self.add_frame, text="+", width=30, command=self.incrementar_cantidad)
        self.incrementar_btn.pack(side="left", padx=5)

        self.dropdown = ctk.CTkOptionMenu(self.add_frame, variable=self.selected_producto, values=["Cargando..."])
        self.dropdown.pack(side="left", padx=5)

        add_button = ctk.CTkButton(self.add_frame, text="Añadir", width=100, command=self.añadir_a_lista)
        add_button.pack(side="left", padx=5)

        # Botón para calcular el precio
        calcular_button = ctk.CTkButton(main_frame, text="Calcular Precio", width=200, command=self.calcular_precio)
        calcular_button.pack(pady=10)

        # Almacena productos añadidos
        self.lista_productos = {}
        self.cargar_productos()

    def cargar_productos(self):
        """Cargar productos desde la base de datos."""
        precios = obtener_precios_productos_por_supermercado()
        if not precios:
            messagebox.showerror("Error", "No se pudo cargar la lista de productos.")
            return

        productos_unicos = set()
        for productos_super in precios.values():
            productos_unicos.update(productos_super.keys())

        self.productos_dict = list(productos_unicos)
        self.dropdown.configure(values=self.productos_dict)
        self.selected_producto.set(self.productos_dict[0] if self.productos_dict else "No hay productos disponibles")

    def añadir_a_lista(self):
        """Añadir un producto con cantidad a la lista."""
        producto = self.selected_producto.get()
        cantidad = self.cantidad_var.get()

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor que 0.")
            return

        cantidad = int(cantidad)
        if producto in self.lista_productos:
            self.lista_productos[producto] += cantidad
        else:
            self.lista_productos[producto] = cantidad

        self.actualizar_lista()

    def actualizar_lista(self):
        """Actualizar visualmente la lista de productos."""
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        for producto, cantidad in self.lista_productos.items():
            item_frame = ctk.CTkFrame(self.lista_frame, fg_color="#3b3b3b", corner_radius=5)
            item_frame.pack(fill="x", padx=5, pady=2)

            ctk.CTkLabel(item_frame, text=f"{producto} x{cantidad}", text_color="white", anchor="w").pack(side="left", padx=5)
            edit_btn = ctk.CTkButton(item_frame, text="Editar", width=50, command=lambda p=producto: self.editar_producto(p))
            edit_btn.pack(side="right", padx=5)

    def editar_producto(self, producto):
        """Abrir una ventana modal para editar la cantidad de un producto."""
        # Ventana modal
        edit_window = ctk.CTkToplevel(self.window)
        edit_window.title("Editar Producto")
        edit_window.geometry("300x300")
        edit_window.resizable(False, False)
        edit_window.grab_set()  # Hacer modal la ventana

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame principal
        main_frame = ctk.CTkFrame(edit_window, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(main_frame, text=f"Editar '{producto}'", font=("Helvetica", 16, "bold"), text_color="white")
        title_label.pack(pady=10)

        # Entrada para nueva cantidad
        ctk.CTkLabel(main_frame, text="Nueva Cantidad:", font=("Helvetica", 14), text_color="white").pack(pady=(5, 0))
        cantidad_var = ctk.StringVar(value=str(self.lista_productos[producto]))
        cantidad_entry = ctk.CTkEntry(main_frame, width=100, textvariable=cantidad_var)
        cantidad_entry.pack(pady=5)

        # Botón Guardar
        def guardar_cantidad():
            nueva_cantidad = cantidad_var.get()
            if nueva_cantidad.isdigit() and int(nueva_cantidad) > 0:
                self.lista_productos[producto] = int(nueva_cantidad)
                self.actualizar_lista()
                edit_window.destroy()
            else:
                messagebox.showerror("Error", "La cantidad debe ser un número mayor que 0.")

        guardar_button = ctk.CTkButton(main_frame, text="Guardar", command=guardar_cantidad, width=100)
        guardar_button.pack(pady=10)

    def incrementar_cantidad(self):
        """Incrementar cantidad en la entrada."""
        cantidad = int(self.cantidad_var.get())
        self.cantidad_var.set(str(cantidad + 1))

    def decrementar_cantidad(self):
        """Decrementar cantidad en la entrada."""
        cantidad = int(self.cantidad_var.get())
        if cantidad > 1:
            self.cantidad_var.set(str(cantidad - 1))

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

        # Recorremos self.lista_productos como un diccionario
        for producto, cantidad in self.lista_productos.items():  # <-- Corregido aquí
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
