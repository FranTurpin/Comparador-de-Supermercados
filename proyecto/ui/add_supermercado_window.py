import tkinter as tk
from tkinter import messagebox
from db.db_operations import add_supermercado

class AddSupermercadoWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Añadir Supermercado")
        self.window.geometry("400x200")
        self.window.configure(bg="#f4f4f4")

        tk.Label(self.window, text="Nombre del supermercado:", font=("Helvetica", 12), bg="#f4f4f4").pack(pady=10)
        self.supermercado_entry = tk.Entry(self.window, font=("Helvetica", 12))
        self.supermercado_entry.pack(pady=5)

        tk.Button(self.window, text="Añadir", width=20, command=self.add_supermercado).pack(pady=20)

    def add_supermercado(self):
        nombre = self.supermercado_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre del supermercado no puede estar vacío.")
            return

        if add_supermercado(nombre):
            messagebox.showinfo("Éxito", f"¡Supermercado '{nombre}' añadido correctamente!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo añadir el supermercado.")
