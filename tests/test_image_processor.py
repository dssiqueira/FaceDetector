import unittest
from app.models.image_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()

    def test_select_image(self):
        # Este teste depende de como select_image está implementado
        img_data = self.processor.select_image()
        self.assertIsNotNone(img_data)

    def test_process_image(self):
        # Supondo que haja uma imagem carregada
        processed_img = self.processor.process_image()
        self.assertIsNotNone(processed_img)

    # Adicione mais testes conforme necessário

if __name__ == "__main__":
    unittest.main()
