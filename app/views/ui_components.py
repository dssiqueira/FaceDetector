import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import os
import subprocess

# Nova paleta de cores mais clara e moderna
COLORS = {
    'bg_main': '#FFFFFF',           # Fundo principal branco
    'bg_sidebar': '#F5F5F5',        # Sidebar cinza muito claro
    'button_bg': '#FFFFFF',         # Botões brancos
    'button_hover': '#F0F0F0',      # Hover suave
    'button_active': '#E8F3FF',     # Azul muito claro quando ativo
    'text': '#2C2C2C',              # Texto quase preto
    'text_secondary': '#6B6B6B',    # Texto secundário cinza
    'accent': '#2563EB',            # Azul vibrante
    'accent_hover': '#1D4ED8',      # Azul mais escuro no hover
    'border': '#E5E5E5',            # Bordas suaves
    'success': '#059669'            # Verde sucesso
}

# Ícones flat em Unicode
ICONS = {
    'select': '',     # Câmera para selecionar
    'process': '',    # Raio para processamento
    'save': '',       # Disco para salvar
    'folder': '',     # Pasta para abrir diretório
    'reset': ''       # Seta circular para reset
}

class CustomButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = kwargs.get('bg', COLORS['button_bg'])
        self.hover_bg = COLORS['button_hover']
        self.active_bg = COLORS['button_active']
        
        self.configure(
            relief="flat",
            borderwidth=1,
            highlightthickness=0,
            font=("SF Pro Display", 13),
        )
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def on_enter(self, e):
        if self['state'] != 'disabled':
            self.config(bg=self.hover_bg)
            
    def on_leave(self, e):
        if self['state'] != 'disabled':
            if hasattr(self, '_active') and self._active:
                self.config(bg=self.active_bg)
            else:
                self.config(bg=self.default_bg)

    def update_state(self, state):
        """Atualiza o estado do botão e seu cursor"""
        self.config(
            state=state,
            cursor="hand2" if state == tk.NORMAL else "arrow"
        )

class Sidebar(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root, bg=COLORS['bg_sidebar'], width=300)
        self.pack(expand=False, fill="y", side="left", anchor="w")
        self.app = app

        # Título da sidebar
        title_frame = tk.Frame(self, bg=COLORS['bg_sidebar'], pady=25)
        title_frame.pack(fill="x")
        title_label = tk.Label(
            title_frame, 
            text="Face Detector", 
            font=("SF Pro Display", 24, "bold"),
            bg=COLORS['bg_sidebar'], 
            fg=COLORS['text']
        )
        title_label.pack()

        # Container para os botões com padding
        button_container = tk.Frame(self, bg=COLORS['bg_sidebar'], padx=20)
        button_container.pack(fill="x", expand=True)

        # Grupo principal de botões
        main_group = tk.Frame(button_container, bg=COLORS['bg_sidebar'])
        main_group.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            main_group,
            text="AÇÕES PRINCIPAIS",
            font=("SF Pro Display", 11),
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_sidebar']
        ).pack(anchor="w", pady=(0, 10))

        self.buttons = []
        self.add_button(ICONS['select'], "Selecionar Imagem", self.app.select_image, "Clique para escolher uma imagem", main_group)
        self.add_button(ICONS['process'], "Processar Imagem", self.app.process_image, "Processa a imagem selecionada", main_group, tk.DISABLED)
        self.add_button(ICONS['save'], "Salvar Recortes", self.app.save_crops, "Salva os rostos detectados", main_group, tk.DISABLED)
        
        # Grupo de utilidades
        utils_group = tk.Frame(button_container, bg=COLORS['bg_sidebar'])
        utils_group.pack(fill="x")
        
        tk.Label(
            utils_group,
            text="UTILIDADES",
            font=("SF Pro Display", 11),
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_sidebar']
        ).pack(anchor="w", pady=(0, 10))

        self.directory_button = self.add_button(ICONS['folder'], "Abrir Pasta", self.open_directory, 
                                              "Abre a pasta com os recortes", utils_group, tk.DISABLED)
        self.reset_button = self.add_button(ICONS['reset'], "Reiniciar", self.app.reset_process, 
                                          "Reinicia o processo", utils_group, tk.DISABLED)

    def add_button(self, icon, text, command, tooltip, container, state=tk.NORMAL):
        button_frame = tk.Frame(container, bg=COLORS['bg_sidebar'])
        button_frame.pack(fill="x", pady=4)
        
        button = CustomButton(
            button_frame,
            text=f"{icon}  {text}",
            bg=COLORS['button_bg'],
            fg=COLORS['text'],
            anchor="w",
            padx=16,
            pady=12,
            command=command,
            state=state,
            cursor="hand2" if state == tk.NORMAL else "arrow"
        )
        button.pack(fill="x")

        self.create_tooltip(button, tooltip)
        self.buttons.append((button_frame, button))
        return button

    def create_tooltip(self, widget, text):
        def enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            tooltip.configure(bg=COLORS['text'])
            label = tk.Label(
                tooltip,
                text=text,
                justify='left',
                background=COLORS['text'],
                foreground=COLORS['button_bg'],
                relief='flat',
                font=("SF Pro Display", 11),
                padx=10,
                pady=6
            )
            label.pack()
            
            widget.tooltip = tooltip

        def leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def highlight_active_button(self, index):
        for i, (frame, button) in enumerate(self.buttons):
            if i == index and button['state'] != 'disabled':
                button.config(bg=COLORS['button_active'])
                button._active = True
                if "highlight" not in frame.children:
                    highlight = tk.Frame(frame, bg=COLORS['accent'], width=3)
                    highlight.place(relheight=1.0, x=0)
            else:
                button.config(bg=COLORS['button_bg'])
                button._active = False
                for child in frame.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.destroy()

    def update_button_state(self, index, state):
        _, button = self.buttons[index]
        button.update_state(state)
        self.highlight_active_button(index)

    def reset_buttons(self):
        for i, (frame, button) in enumerate(self.buttons):
            button.update_state(tk.DISABLED)
        _, button = self.buttons[0]
        button.update_state(tk.NORMAL)
        self.highlight_active_button(0)

    def enable_directory_and_reset_buttons(self):
        self.directory_button.update_state(tk.NORMAL)
        self.reset_button.update_state(tk.NORMAL)

    def open_directory(self):
        folder_path = self.app.processor.get_crop_dir()
        print(f"Tentando abrir diretório: {folder_path}")
        
        if os.path.exists(folder_path):
            try:
                # No macOS, usar o comando 'open'
                subprocess.run(['open', folder_path])
                print(f"Diretório aberto com sucesso: {folder_path}")
            except Exception as e:
                print(f"Erro ao abrir diretório: {e}")
                messagebox.showerror("Erro", f"Não foi possível abrir o diretório: {e}")
        else:
            print(f"Diretório não encontrado: {folder_path}")
            messagebox.showerror("Erro", "O diretório não existe.")

class SuccessMessage(tk.Label):
    def __init__(self, root, text):
        super().__init__(
            root,
            text=" " + text,
            font=("SF Pro Display", 13),
            bg=COLORS['success'],
            fg=COLORS['button_bg'],
            pady=12,
            padx=25,
            relief="flat"
        )
        # Mostrar a mensagem imediatamente
        self.place(relx=0.5, rely=0.05, anchor="n")
        # Configurar o fade out após 4 segundos
        self.after(4000, self.fade_out)

    def fade_out(self):
        """Inicia a animação de fade out"""
        self.alpha = 1.0
        self.fade()

    def fade(self):
        """Executa a animação de fade out gradualmente"""
        if self.alpha > 0:
            self.alpha -= 0.1
            self.configure(bg=self._fade_color(COLORS['success'], self.alpha))
            self.after(50, self.fade)
        else:
            self.destroy()

    def _fade_color(self, color, alpha):
        """Calcula a cor com transparência para o fade"""
        # Converter cor hex para RGB
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        # Misturar com o fundo branco baseado no alpha
        r = int(r * alpha + 255 * (1 - alpha))
        g = int(g * alpha + 255 * (1 - alpha))
        b = int(b * alpha + 255 * (1 - alpha))
        
        return f'#{r:02x}{g:02x}{b:02x}'

class Footer(tk.Frame):
    def __init__(self, root, version=""):
        super().__init__(root, bg=COLORS['bg_main'])
        footer_content = tk.Frame(self, bg=COLORS['bg_main'])
        footer_content.pack(expand=True)

        # Label com o texto e o link
        label = tk.Label(
            footer_content,
            text="Feito com  por ",
            font=("SF Pro Display", 11),
            bg=COLORS['bg_main'],
            fg=COLORS['text_secondary']
        )
        label.pack(side="left")

        # Link para o site
        link = tk.Label(
            footer_content,
            text="Dsiqueira",
            font=("SF Pro Display", 11, "underline"),
            fg=COLORS['accent'],
            bg=COLORS['bg_main'],
            cursor="hand2"
        )
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://dsiqueira.com"))
        link.bind("<Enter>", lambda e: link.configure(fg=COLORS['accent_hover']))
        link.bind("<Leave>", lambda e: link.configure(fg=COLORS['accent']))

        # Versão do aplicativo
        version_label = tk.Label(
            footer_content,
            text=" - " + version,
            font=("SF Pro Display", 11),
            bg=COLORS['bg_main'],
            fg=COLORS['text_secondary']
        )
        version_label.pack(side="left")

        footer_content.pack(expand=True, pady=15)
