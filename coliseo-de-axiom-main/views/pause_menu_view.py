import pygame

class PauseMenuView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        self.font_title = pygame.font.Font(None, 74)
        self.font_button = pygame.font.Font(None, 50)
        
        self.colors = {
            "overlay": (0, 0, 0, 128),  # Negro semi-transparente
            "white": (255, 255, 255),
            "button_bg": (100, 100, 100),
            "button_hover_bg": (150, 150, 150),
            "text": (230, 230, 230)
        }
        self.button_rects = []

    def draw(self):
        # Crear superficie semi-transparente
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill(self.colors["overlay"])
        self.screen.blit(overlay, (0, 0))
        
        # Título
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2 - 100
        
        title_surface = self.font_title.render(self.model.get_title(), True, self.colors["white"])
        title_rect = title_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(title_surface, title_rect)

        # Botones
        self.button_rects = []
        button_labels = self.model.get_button_labels()
        button_width = 250
        button_height = 60
        button_spacing = 20
        start_y = center_y + 50
        
        mouse_pos = pygame.mouse.get_pos()

        for i, label in enumerate(button_labels):
            button_x = center_x - (button_width // 2)
            button_y = start_y + i * (button_height + button_spacing)
            
            rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.button_rects.append(rect)

            bg_color = self.colors["button_hover_bg"] if rect.collidepoint(mouse_pos) else self.colors["button_bg"]
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
            
            text_surface = self.font_button.render(label, True, self.colors["text"])
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
            
        pygame.display.flip()

    def get_button_rects(self):
        return self.button_rects