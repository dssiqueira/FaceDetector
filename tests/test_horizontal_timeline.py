import unittest
from tkinter import Tk
from app.views.horizontal_timeline import HorizontalTimeline

class TestHorizontalTimeline(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.timeline = HorizontalTimeline(self.root)

    def test_timeline_initialization(self):
        self.assertEqual(self.timeline.steps, 3)

    def test_update_progress(self):
        self.timeline.update_progress(2)
        self.assertEqual(self.timeline.current_step, 2)

    # Adicione mais testes conforme necessário

if __name__ == "__main__":
    unittest.main()
