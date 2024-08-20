import cv2
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self):
        self.file_name = ""
        self.image = None
        self.faces = None
        self.crop_dir = "crop"

    def select_image(self):
        self.file_name = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
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
        os.makedirs(self.crop_dir, exist_ok=True)
        cropped_images = []
        for i, (x, y, w, h) in enumerate(self.faces):
            cropped_img = self.image[y:y+h, x:x+w]
            cropped_images.append(ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))))
        return cropped_images

    def get_crop_dir(self):
        return self.crop_dir
