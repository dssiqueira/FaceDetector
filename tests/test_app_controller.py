import unittest
from tkinter import Tk
from app.controllers.app_controller import AppController

class TestAppController(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = AppController(self.root)

    def test_initialization(self):
        self.assertEqual(self.app.steps_completed, [False, False, False])
        self.assertIsNotNone(self.app.sidebar)
        self.assertIsNotNone(self.app.timeline)
        self.assertIsNotNone(self.app.main_area)

    def test_select_image(self):
        # Supondo que o método de seleção de imagem retorne uma imagem válida
        self.app.select_image()
        self.assertTrue(self.app.steps_completed[0])

    # Adicione mais testes conforme necessário

if __name__ == "__main__":
    unittest.main()
