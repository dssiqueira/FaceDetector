import cv2
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self):
        self.file_name = ""
        self.image = None
        self.faces = None
        # Criar o diretório 'crops' na raiz do projeto
        self.crop_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'crops')
        print(f"Diretório de recortes configurado: {self.crop_dir}")

    def select_image(self):
        self.file_name = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if self.file_name:
            self.image = cv2.imread(self.file_name)
            return self.get_image_data()
        return None

    def get_image_data(self):
        image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        return ImageTk.PhotoImage(image)

    def process_image(self):
        if self.image is None:
            messagebox.showerror("Erro", "Nenhuma imagem selecionada.")
            return None
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if self.faces is None or len(self.faces) == 0:
            messagebox.showinfo("Resultado", "Nenhum rosto foi detectado na imagem.")
            return None

        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        return self.get_image_data()

    def display_image(self, img_data, panel):
        panel.config(image=img_data)
        panel.image = img_data

    def save_crops(self):
        print("Iniciando salvamento dos recortes...")
        
        # Criar diretório se não existir
        if not os.path.exists(self.crop_dir):
            os.makedirs(self.crop_dir)
            print(f"Diretório {self.crop_dir} criado")
        
        # Limpar diretório de recortes anteriores
        for file in os.listdir(self.crop_dir):
            file_path = os.path.join(self.crop_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Arquivo antigo removido: {file_path}")
            except Exception as e:
                print(f'Erro ao deletar {file_path}: {e}')

        # Salvar novos recortes
        cropped_images = []
        for i, (x, y, w, h) in enumerate(self.faces):
            # Recortar a face
            cropped_img = self.image[y:y+h, x:x+w]
            
            # Converter para RGB (PIL usa RGB)
            cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
            
            # Criar objeto PIL Image
            pil_img = Image.fromarray(cropped_img_rgb)
            
            # Salvar no disco
            file_path = os.path.join(self.crop_dir, f'face_{i+1}.png')
            pil_img.save(file_path, 'PNG')
            print(f"Recorte salvo: {file_path}")
            
            # Criar thumbnail para exibição
            cropped_images.append(ImageTk.PhotoImage(pil_img))
        
        print(f"Total de recortes salvos: {len(cropped_images)}")
        return cropped_images

    def get_crop_dir(self):
        return self.crop_dir  # Já é um caminho absoluto
