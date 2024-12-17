import customtkinter as ctk
from ui.login_window import LoginWindow
from ui.signup_window import SignUpWindow

class MainWindow:
    def __init__(self, root):
        # Configuración inicial de la ventana principal
        self.root = root
        self.root.title("Bienvenido a Comparador App")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        # Aplicar tema oscuro
        ctk.set_appearance_mode("dark")  # Tema oscuro
        ctk.set_default_color_theme("blue")

        # Crear un Frame que cubra toda la ventana para el fondo gris oscuro
        background_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="#2b2b2b")
        background_frame.pack(fill="both", expand=True)

        # Etiqueta de título
        title_label = ctk.CTkLabel(background_frame, text="Comparador de Supermercados",
                                   font=("Helvetica", 24, "bold"), text_color="white")
        title_label.pack(pady=50)

        # Botón Log In
        login_button = ctk.CTkButton(background_frame, text="Log In", command=self.open_login, width=200)
        login_button.pack(pady=10)

        # Botón Sign Up
        signup_button = ctk.CTkButton(background_frame, text="Sign Up", command=self.open_signup, width=200)
        signup_button.pack(pady=10)

        # Botón Salir
        exit_button = ctk.CTkButton(background_frame, text="Salir", command=self.root.destroy,
                                    fg_color="red", hover_color="#cc0000", width=200)
        exit_button.pack(pady=10)

    def open_login(self):
        LoginWindow(self.root)

    def open_signup(self):
        SignUpWindow(self.root)


# Ejecución de la ventana principal
if __name__ == "__main__":
    app = ctk.CTk()  # Crear ventana principal con CustomTkinter
    MainWindow(app)
    app.mainloop()
