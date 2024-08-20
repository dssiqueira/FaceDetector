from tkinter import Tk
from app.controllers.app_controller import AppController

if __name__ == "__main__":
    root = Tk()
    app = AppController(root)
    root.mainloop()
