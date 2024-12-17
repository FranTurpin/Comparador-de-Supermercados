import tkinter as tk
from ui.lista_window import ListaWindow
from ui.eliminar_window import EliminarWindow
from ui.add_product_window import AddProductWindow
from ui.add_supermercado_window import AddSupermercadoWindow
from ui.eliminar_supermercado_window import EliminarSupermercadoWindow  # Nueva ventana

class MainMenuWindow:
    def __init__(self, root, username):
        self.window = tk.Toplevel(root)
        self.window.title("Menú Principal")
        self.window.geometry("400x500")
        self.window.configure(bg="#fafafa")

        tk.Label(self.window, text=f"¡Bienvenido, {username}!", font=("Helvetica", 14, "bold"), bg="#fafafa").pack(pady=10)

        # Botones para navegar a otras ventanas
        tk.Button(self.window, text="Crear lista de la compra", width=24, height=2,
                  command=self.open_lista_window).pack(pady=10)

        tk.Button(self.window, text="Añadir productos", width=24, height=2,
                  command=self.open_add_product_window).pack(pady=10)

        tk.Button(self.window, text="Añadir supermercado", width=24, height=2,
                  command=self.open_add_supermercado_window).pack(pady=10)

        tk.Button(self.window, text="Eliminar producto", width=24, height=2,
                  command=self.open_eliminar_window).pack(pady=10)

        # Nuevo botón para eliminar supermercado
        tk.Button(self.window, text="Eliminar supermercado", width=24, height=2,
                  command=self.open_eliminar_supermercado_window).pack(pady=10)

        # Botón para salir
        tk.Button(self.window, text="Salir", width=24, height=2, command=self.window.destroy).pack(pady=10)

    def open_lista_window(self):
        """Abre la ventana para crear una lista de la compra."""
        ListaWindow(self.window)

    def open_add_product_window(self):
        """Abre la ventana para añadir un producto."""
        AddProductWindow(self.window)

    def open_add_supermercado_window(self):
        """Abre la ventana para añadir un nuevo supermercado."""
        AddSupermercadoWindow(self.window)

    def open_eliminar_window(self):
        """Abre la ventana para eliminar un producto."""
        EliminarWindow(self.window)

    def open_eliminar_supermercado_window(self):
        """Abre la ventana para eliminar un supermercado."""
        EliminarSupermercadoWindow(self.window)
