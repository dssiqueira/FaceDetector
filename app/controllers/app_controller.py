import tkinter as tk
from app.views.ui_components import Sidebar, SuccessMessage, Footer
from app.views.horizontal_timeline import HorizontalTimeline
from app.models.image_processor import ImageProcessor
import os
from PIL import Image, ImageTk

# Nova paleta de cores mais clara e moderna
COLORS = {
    'bg_main': '#FFFFFF',           # Fundo principal branco
    'bg_content': '#FFFFFF',        # Área de conteúdo branca
    'bg_sidebar': '#F5F5F5',        # Sidebar cinza muito claro
    'border': '#E5E5E5',            # Bordas suaves
}

class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detector")

        # Definir ícone
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'img', 'icon.png')
            if os.path.exists(icon_path):
                # Carregar e converter o ícone usando PIL
                icon_image = Image.open(icon_path)
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, icon_photo)
                # Manter uma referência para evitar que o garbage collector remova a imagem
                self._icon = icon_photo
        except Exception as e:
            print(f"Não foi possível carregar o ícone: {e}")

        # Definir tamanho inicial e cor de fundo
        self.root.geometry("1200x800")
        self.root.configure(bg=COLORS['bg_main'])

        # Frame principal
        self.main_frame = tk.Frame(root, bg=COLORS['bg_main'])
        self.main_frame.pack(expand=True, fill="both", side="top")

        # Processador de imagem
        self.processor = ImageProcessor()

        # Menu Lateral
        self.sidebar = Sidebar(self.main_frame, self)

        # Área Principal com borda suave
        self.main_area = tk.Frame(
            self.main_frame,
            bg=COLORS['bg_content'],
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )
        self.main_area.pack(expand=True, fill="both", side="right", padx=30, pady=30)

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
        self.image_panel = tk.Label(self.main_area, bg=COLORS['bg_content'], relief="groove", bd=1)
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
        print("Iniciando processo de salvamento...")
        if self.steps_completed[1]:
            for widget in self.main_area.winfo_children():
                if isinstance(widget, tk.Label) and widget != self.image_panel:
                    widget.destroy()

            print("Chamando processor.save_crops()...")
            cropped_images = self.processor.save_crops()
            print(f"Recortes retornados: {len(cropped_images)}")

            self.image_panel.pack_forget()
            for img in cropped_images:
                label = tk.Label(self.main_area, image=img, bg=COLORS['bg_content'], relief="groove", bd=1)
                label.pack(pady=10, fill="both", expand="yes")
                label.image = img
            
            print("Mostrando mensagem de sucesso...")
            SuccessMessage(self.main_area, "Recortes salvos com sucesso!")  # Removido .show()
            
            print("Habilitando botões...")
            self.sidebar.enable_directory_and_reset_buttons()
            
            print("Atualizando timeline...")
            self.timeline.update_progress(3)
            
            print("Marcando passo como completo...")
            self.steps_completed[2] = True
            print("Processo de salvamento concluído!")

    def reset_process(self):
        # Limpar o estado
        self.steps_completed = [False, False, False]
        self.timeline.reset_timeline()
        
        # Resetar a interface
        for widget in self.main_area.winfo_children():
            widget.destroy()
        self.create_timeline()
        self.create_image_panel()
        
        # Resetar os botões
        self.sidebar.reset_buttons()
