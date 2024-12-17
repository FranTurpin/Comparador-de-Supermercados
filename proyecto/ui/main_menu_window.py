import customtkinter as ctk

class MainMenuWindow:
    def __init__(self, root, username):
        self.window = ctk.CTkToplevel(root)  # Crear ventana secundaria
        self.window.title("Menú Principal")
        self.window.geometry("400x500")
        self.window.resizable(False, False)

        # Configurar tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame principal con fondo oscuro
        main_frame = ctk.CTkFrame(self.window, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Etiqueta de bienvenida
        title_label = ctk.CTkLabel(main_frame, text=f"¡Bienvenido, {username}!",
                                   font=("Helvetica", 18, "bold"), text_color="white")
        title_label.pack(pady=20)

        # Botones para navegar a otras ventanas
        ctk.CTkButton(main_frame, text="Crear lista de la compra", width=220, height=40,
                      command=self.open_lista_window).pack(pady=10)

        ctk.CTkButton(main_frame, text="Añadir productos", width=220, height=40,
                      command=self.open_add_product_window).pack(pady=10)

        ctk.CTkButton(main_frame, text="Añadir supermercado", width=220, height=40,
                      command=self.open_add_supermercado_window).pack(pady=10)

        ctk.CTkButton(main_frame, text="Eliminar producto", width=220, height=40,
                      command=self.open_eliminar_window).pack(pady=10)

        ctk.CTkButton(main_frame, text="Eliminar supermercado", width=220, height=40,
                      command=self.open_eliminar_supermercado_window).pack(pady=10)

        # Botón para salir
        ctk.CTkButton(main_frame, text="Salir", width=220, height=40, fg_color="red",
                      hover_color="#cc0000", command=self.window.destroy).pack(pady=10)

        # Hacer la ventana modal
        self.window.grab_set()

    # Métodos con importaciones locales para evitar ciclos de importación
    def open_lista_window(self):
        """Abre la ventana para crear una lista de la compra."""
        from ui.lista_window import ListaWindow  # Importación local
        ListaWindow(self.window)

    def open_add_product_window(self):
        """Abre la ventana para añadir un producto."""
        from ui.add_product_window import AddProductWindow  # Importación local
        AddProductWindow(self.window)

    def open_add_supermercado_window(self):
        """Abre la ventana para añadir un nuevo supermercado."""
        from ui.add_supermercado_window import AddSupermercadoWindow  # Importación local
        AddSupermercadoWindow(self.window)

    def open_eliminar_window(self):
        """Abre la ventana para eliminar un producto."""
        from ui.eliminar_window import EliminarWindow  # Importación local
        EliminarWindow(self.window)

    def open_eliminar_supermercado_window(self):
        """Abre la ventana para eliminar un supermercado."""
        from ui.eliminar_supermercado_window import EliminarSupermercadoWindow  # Importación local
        EliminarSupermercadoWindow(self.window)
