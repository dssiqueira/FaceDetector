import tkinter as tk

class HorizontalTimeline(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg="#1F1F1F", height=60)
        self.canvas = tk.Canvas(self, height=50, bg="#1F1F1F", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.steps = 3
        self.initialized = False  # Controle de inicialização
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event=None):
        if not self.initialized:
            self.initialized = True
            self.after(100, self.draw_timeline)  # Desenha a timeline após a janela carregar
        else:
            self.draw_timeline()

    def draw_timeline(self, event=None):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        total_width = 600  # Largura fixa da timeline para 3 steps
        x_offset = (width - total_width) // 2  # Calcula o deslocamento para centralizar
        side_length = 30
        line_y = 25

        for i in range(self.steps):
            x_position = x_offset + i * 200 + 100

            if i < self.steps - 1:
                self.canvas.create_line(x_position + side_length // 2, line_y, x_position + 200 - side_length // 2, line_y, fill="#D3D3D3", width=3)
            
            square_color = "#D3D3D3"
            self.canvas.create_rectangle(x_position - side_length // 2, line_y - side_length // 2, x_position + side_length // 2, line_y + side_length // 2, fill=square_color, outline="#D3D3D3", width=2)
            self.canvas.create_text(x_position, line_y, text=f"{i + 1}", fill="white", font=("Segoe UI", 12, "bold"))

    def update_progress(self, step):
        self.draw_timeline()
        width = self.canvas.winfo_width()
        total_width = 600
        x_offset = (width - total_width) // 2
        side_length = 30
        line_y = 25

        for i in range(step):
            x_position = x_offset + i * 200 + 100
            self.canvas.create_rectangle(x_position - side_length // 2, line_y - side_length // 2, x_position + side_length // 2, line_y + side_length // 2, fill="#323130", outline="#0078D4", width=2)
            self.canvas.create_text(x_position, line_y, text=f"{i + 1}", fill="white", font=("Segoe UI", 12, "bold"))

    def reset_timeline(self):
        self.draw_timeline()
