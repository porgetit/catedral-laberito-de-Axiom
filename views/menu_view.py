# view.py
import pygame

class MenuView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        self.font_title = pygame.font.Font(None, 74)
        self.font_button = pygame.font.Font(None, 50)
        
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "button_bg": (100, 100, 100),
            "button_hover_bg": (150, 150, 150),
            "text": (230, 230, 230),
            "background": (30, 30, 50) # Un azul oscuro
        }
        self.button_rects = []

    def _render_text(self, text, font, color, center_pos):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center_pos)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw(self):
        self.screen.fill(self.colors["background"])
        
        # Título
        title_center_x = self.screen.get_width() // 2
        title_center_y = self.screen.get_height() // 4
        self._render_text(self.model.get_title(), self.font_title, self.colors["white"], (title_center_x, title_center_y))

        # Botones
        self.button_rects = [] # Limpiar rects anteriores para recalcular en cada frame
        button_labels = self.model.get_button_labels()
        button_width = 250
        button_height = 60
        button_spacing = 20
        start_y = title_center_y + 100 # Posición inicial Y para el primer botón
        
        mouse_pos = pygame.mouse.get_pos()

        for i, label in enumerate(button_labels):
            button_x = title_center_x - (button_width // 2)
            button_y = start_y + i * (button_height + button_spacing)
            
            rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.button_rects.append(rect) # Guardar el rect para el controlador

            # Efecto hover
            bg_color = self.colors["button_bg"]
            if rect.collidepoint(mouse_pos):
                bg_color = self.colors["button_hover_bg"]
            
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
            self._render_text(label, self.font_button, self.colors["text"], rect.center)
            
        pygame.display.flip()

    def get_button_rects(self):
        # Devuelve los rectángulos de los botones para que el controlador los use
        return self.button_rects