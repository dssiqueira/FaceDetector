import tkinter as tk

# Nova paleta de cores mais clara e moderna
COLORS = {
    'bg_main': '#FFFFFF',           # Fundo principal branco
    'bg_timeline': '#F5F5F5',       # Timeline cinza muito claro
    'step_bg': '#FFFFFF',           # Passos brancos
    'step_hover': '#F0F0F0',        # Hover suave
    'step_active': '#E8F3FF',       # Azul muito claro quando ativo
    'text': '#2C2C2C',              # Texto quase preto
    'text_secondary': '#6B6B6B',    # Texto secundário cinza
    'accent': '#2563EB',            # Azul vibrante
    'accent_hover': '#1D4ED8',      # Azul mais escuro no hover
    'border': '#E5E5E5',            # Bordas suaves
    'success': '#059669'            # Verde sucesso
}

class HorizontalTimeline(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg=COLORS['bg_main'])
        self.canvas = tk.Canvas(
            self,
            height=100,
            bg=COLORS['bg_main'],
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, pady=20)
        self.steps = 3
        self.initialized = False
        self.step_labels = ["Selecionar", "Processar", "Salvar"]
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event=None):
        if not self.initialized:
            self.initialized = True
            self.after(100, self.draw_timeline)
        else:
            self.draw_timeline()

    def draw_timeline(self, event=None):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        total_width = 600
        x_offset = (width - total_width) // 2
        side_length = 40
        line_y = 30

        # Desenha as linhas de conexão primeiro (background)
        for i in range(self.steps - 1):
            x_position = x_offset + i * 200 + 100
            self.canvas.create_line(
                x_position + side_length // 2, line_y,
                x_position + 200 - side_length // 2, line_y,
                fill=COLORS['border'],
                width=2,
                dash=(4, 4)  # Linha pontilhada
            )

        # Desenha os círculos e textos
        for i in range(self.steps):
            x_position = x_offset + i * 200 + 100

            # Círculo de fundo com borda suave
            self.canvas.create_oval(
                x_position - side_length // 2, line_y - side_length // 2,
                x_position + side_length // 2, line_y + side_length // 2,
                fill=COLORS['step_bg'],
                outline=COLORS['border'],
                width=1
            )
            
            # Número do passo
            self.canvas.create_text(
                x_position, line_y,
                text=f"{i + 1}",
                fill=COLORS['text'],
                font=("SF Pro Display", 16, "bold")
            )
            
            # Label do passo
            self.canvas.create_text(
                x_position, line_y + 40,
                text=self.step_labels[i],
                fill=COLORS['text_secondary'],
                font=("SF Pro Display", 13)
            )

    def update_progress(self, step):
        self.draw_timeline()
        width = self.canvas.winfo_width()
        total_width = 600
        x_offset = (width - total_width) // 2
        side_length = 40
        line_y = 30

        # Atualiza as linhas de conexão completadas
        for i in range(step - 1):
            x_position = x_offset + i * 200 + 100
            self.canvas.create_line(
                x_position + side_length // 2, line_y,
                x_position + 200 - side_length // 2, line_y,
                fill=COLORS['accent'],
                width=2
            )

        # Atualiza os círculos completados
        for i in range(step):
            x_position = x_offset + i * 200 + 100
            
            # Círculo de progresso
            self.canvas.create_oval(
                x_position - side_length // 2, line_y - side_length // 2,
                x_position + side_length // 2, line_y + side_length // 2,
                fill=COLORS['accent'],
                outline=COLORS['accent'],
                width=1
            )
            
            # Checkmark ou número
            if i < step - 1:
                self.canvas.create_text(
                    x_position, line_y,
                    text="✓",
                    fill=COLORS['bg_main'],
                    font=("SF Pro Display", 18, "bold")
                )
            else:
                self.canvas.create_text(
                    x_position, line_y,
                    text=f"{i + 1}",
                    fill=COLORS['bg_main'],
                    font=("SF Pro Display", 16, "bold")
                )
            
            # Label do passo (mais escuro para passos completados)
            self.canvas.create_text(
                x_position, line_y + 40,
                text=self.step_labels[i],
                fill=COLORS['text'],
                font=("SF Pro Display", 13)
            )

    def reset_timeline(self):
        self.draw_timeline()
