import tkinter as tk
from app.views.ui_components import Sidebar, SuccessMessage, Footer
from app.views.horizontal_timeline import HorizontalTimeline
from app.models.image_processor import ImageProcessor

class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detector")

        # Definir ícone
        icon = tk.PhotoImage(file='assets/img/icon.png')
        self.root.iconphoto(True, icon)

        # Definir tamanho inicial
        self.root.geometry("1200x800")

        # Frame principal
        self.main_frame = tk.Frame(root, bg="#2D2D2D")
        self.main_frame.pack(expand=True, fill="both", side="top")

        # Processador de imagem
        self.processor = ImageProcessor()

        # Menu Lateral
        self.sidebar = Sidebar(self.main_frame, self)

        # Área Principal
        self.main_area = tk.Frame(self.main_frame, bg="#1F1F1F")
        self.main_area.pack(expand=True, fill="both", side="right", padx=20, pady=20)

        # Timeline Horizontal
        self.create_timeline()

        # Painel de imagem
        self.create_image_panel()

        # Rodapé com versão
        self.footer = Footer(root, version="Versão 1.0")
        self.footer.pack(side="bottom", fill="x")

        # Variáveis para controlar os passos
        self.steps_completed = [False, False, False]

    def create_timeline(self):
        self.timeline = HorizontalTimeline(self.main_area)
        self.timeline.pack(fill="x", pady=10)

    def create_image_panel(self):
        self.image_panel = tk.Label(self.main_area, bg="#323130", relief="groove", bd=1)
        self.image_panel.pack(pady=20, fill="both", expand="yes")

    def update_image_display(self, img_data):
        self.processor.display_image(img_data, self.image_panel)

    def select_image(self):
        img_data = self.processor.select_image()
        if img_data:
            self.update_image_display(img_data)
            self.steps_completed[0] = True
            self.sidebar.update_button_state(1, tk.NORMAL)
            self.timeline.update_progress(1)

    def process_image(self):
        if self.steps_completed[0]:
            processed_img = self.processor.process_image()
            if processed_img:
                self.update_image_display(processed_img)
                self.steps_completed[1] = True
                self.sidebar.update_button_state(2, tk.NORMAL)
                self.timeline.update_progress(2)

    def save_crops(self):
        if self.steps_completed[1]:
            for widget in self.main_area.winfo_children():
                if isinstance(widget, tk.Label) and widget != self.image_panel:
                    widget.destroy()

            cropped_images = self.processor.save_crops()
            self.image_panel.pack_forget()
            for img in cropped_images:
                label = tk.Label(self.main_area, image=img, bg="#323130", relief="groove", bd=1)
                label.pack(pady=10, fill="both", expand="yes")
                label.image = img
            SuccessMessage(self.main_area, "Recortes salvos com sucesso!").show()
            self.sidebar.enable_directory_and_reset_buttons()
            self.timeline.update_progress(3)
            self.steps_completed[2] = True

    def reset_process(self):
        self.steps_completed = [False, False, False]
        self.sidebar.reset_buttons()
        for widget in self.main_area.winfo_children():
            widget.destroy()
        self.create_timeline()
        self.create_image_panel()
        self.sidebar.enable_directory_and_reset_buttons()
