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

        ctk.set_appearance_mode("dark")  # Tema oscuro
        ctk.set_default_color_theme("blue")
        root.configure(fg_color="#2b2b2b")  # Gris oscuro personalizado

        # Frame principal
        frame = ctk.CTkFrame(root, fg_color="#2b2b2b", corner_radius=0)
        frame.pack(fill="both", expand=True)

        # Etiqueta de título
        title_label = ctk.CTkLabel(frame, text="Comparador de Supermercados",
                                   font=("Helvetica", 24, "bold"), text_color="white")
        title_label.pack(pady=50)

        # Botones
        login_button = ctk.CTkButton(frame, text="Log In", command=self.open_login, width=200)
        login_button.pack(pady=10)

        signup_button = ctk.CTkButton(frame, text="Sign Up", command=self.open_signup, width=200)
        signup_button.pack(pady=10)

        exit_button = ctk.CTkButton(frame, text="Salir", command=self.root.destroy, fg_color="red",
                                    hover_color="#cc0000", width=200)
        exit_button.pack(pady=10)

    def open_login(self):
        LoginWindow(self.root)  # Abre la ventana de Log In

    def open_signup(self):
        SignUpWindow(self.root)  # Abre la ventana de Sign Up


# Ejecución de la ventana principal
if __name__ == "__main__":
    app = ctk.CTk()
    MainWindow(app)
    app.mainloop()
