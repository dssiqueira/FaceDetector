import tkinter as tk
from tkinter import messagebox
import webbrowser
import os

class Sidebar(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root, bg="#1F1F1F", width=220)
        self.pack(expand=False, fill="y", side="left", anchor="w")
        self.app = app

        # Ícones e botões laterais (Estilo Windows 11)
        self.buttons = []
        self.add_button("📁", "Selecionar Imagem", self.app.select_image)
        self.add_button("⚙️", "Processar Imagem", self.app.process_image, state=tk.DISABLED)
        self.add_button("💾", "Salvar Recortes", self.app.save_crops, state=tk.DISABLED)

        # Botão de Abrir Diretório e Reiniciar
        self.directory_button = self.add_button("📂", "Abrir Pasta", self.open_directory, state=tk.DISABLED)
        self.reset_button = self.add_button("🔄", "Reiniciar", self.app.reset_process, state=tk.DISABLED)

    def add_button(self, icon, text, command, state=tk.NORMAL):
        button_frame = tk.Frame(self, bg="#2D2D2D")
        button_frame.pack(fill="x", padx=5, pady=2)
        icon_label = tk.Label(button_frame, text=icon, font=("Segoe UI", 16), fg="#FFFFFF", bg="#2D2D2D")
        icon_label.pack(side="left", padx=10)
        button = tk.Button(button_frame, text=text, font=("Segoe UI", 12), bg="#2D2D2D", fg="white", anchor="w",
                           relief="flat", padx=10, pady=10, command=command, state=state, cursor="hand2")
        button.pack(side="left", fill="x", expand=True)

        self.buttons.append((button_frame, button))
        return button

    def update_button_state(self, index, state):
        _, button = self.buttons[index]
        button.config(state=state)
        self.highlight_active_button(index)

    def reset_buttons(self):
        for i, (frame, button) in enumerate(self.buttons):
            button.config(state=tk.DISABLED)
        _, button = self.buttons[0]
        button.config(state=tk.NORMAL)
        self.highlight_active_button(0)

    def enable_directory_and_reset_buttons(self):
        self.directory_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)

    def highlight_active_button(self, index):
        for i, (frame, button) in enumerate(self.buttons):
            if i == index:
                frame.config(bg="#3E3E3E")
                button.config(bg="#3E3E3E")
                frame.children["highlight"] = tk.Frame(frame, bg="#0078D4", width=2)
                frame.children["highlight"].pack(side="left", fill="y")
            else:
                frame.config(bg="#2D2D2D")
                button.config(bg="#2D2D2D")
                if "highlight" in frame.children:
                    frame.children["highlight"].destroy()

    def open_directory(self):
        folder_path = self.app.processor.get_crop_dir()
        if os.path.exists(folder_path):
            webbrowser.open(os.path.realpath(folder_path))
        else:
            messagebox.showerror("Erro", "O diretório não existe.")

class SuccessMessage(tk.Label):
    def __init__(self, root, text):
        super().__init__(root, text=text, font=("Segoe UI", 12), bg="#D4EDDA", fg="#155724", pady=10, padx=20, relief="solid", bd=1)
        self.place(relx=0.5, rely=0.1, anchor="n")
        self.after(5000, self.destroy)

    def show(self):
        self.place(relx=0.5, rely=0.1, anchor="n")

class Footer(tk.Frame):
    def __init__(self, root, version=""):
        super().__init__(root, bg="#1F1F1F")
        footer_content = tk.Frame(self, bg="#1F1F1F")
        footer_content.pack(expand=True)

        # Label com o texto e o link
        label = tk.Label(
            footer_content, text="Feito com 💖 por ", font=("Segoe UI", 10),
            bg="#1F1F1F", fg="white"
        )
        label.pack(side="left")

        # Link para o site de Dsiqueira
        link = tk.Label(
            footer_content, text="Dsiqueira", font=("Segoe UI", 10, "underline"),
            fg="lightblue", bg="#1F1F1F", cursor="hand2"
        )
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://dsiqueira.com"))

        # Label com a versão do aplicativo
        version_label = tk.Label(
            footer_content, text=" - " + version, font=("Segoe UI", 10),
            bg="#1F1F1F", fg="white"
        )
        version_label.pack(side="left")

        footer_content.pack(expand=True, pady=10)


