import tkinter as tk
from tkinter import messagebox
from db.db_operations import eliminar_supermercado, obtener_supermercados

class EliminarSupermercadoWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Eliminar Supermercado")
        self.window.geometry("400x200")
        self.window.configure(bg="#f4f4f4")

        # Título
        tk.Label(self.window, text="Eliminar Supermercado", font=("Helvetica", 14), bg="#f4f4f4").pack(pady=10)

        # Cargar supermercados
        self.supermercados = [supermercado['nombre'] for supermercado in obtener_supermercados()]
        self.selected_supermercado = tk.StringVar(self.window)
        self.selected_supermercado.set(self.supermercados[0] if self.supermercados else "No hay supermercados")

        # Desplegable
        self.dropdown = tk.OptionMenu(self.window, self.selected_supermercado, *self.supermercados)
        self.dropdown.pack(pady=10)

        # Botón Eliminar
        tk.Button(self.window, text="Eliminar", command=self.eliminar).pack(pady=10)

    def eliminar(self):
        nombre = self.selected_supermercado.get()
        if not nombre or nombre == "No hay supermercados":
            messagebox.showerror("Error", "Selecciona un supermercado válido.")
            return

        if eliminar_supermercado(nombre):
            messagebox.showinfo("Éxito", f"¡Supermercado '{nombre}' eliminado correctamente!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", f"No se pudo eliminar el supermercado '{nombre}'.")
