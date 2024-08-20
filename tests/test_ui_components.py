import unittest
from tkinter import Tk
from app.views.ui_components import Sidebar, Footer

class TestUIComponents(unittest.TestCase):
    def setUp(self):
        self.root = Tk()

    def test_sidebar_creation(self):
        sidebar = Sidebar(self.root, None)
        self.assertIsNotNone(sidebar)

    def test_footer_creation(self):
        footer = Footer(self.root, version="1.0")
        self.assertIn("1.0", footer.children.values()[0].cget("text"))

    # Adicione mais testes conforme necessário

if __name__ == "__main__":
    unittest.main()
