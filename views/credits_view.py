import pygame
from models.credits import CreditsModel

class CreditsView:
    def __init__(self, screen, model: CreditsModel):
        self.screen = screen
        self.model = model
        pygame.font.init()
        self.font_title = pygame.font.Font(None, 74)
        self.font_text = pygame.font.Font(None, 36)
        self.font_back = pygame.font.Font(None, 50)

        self.colors = {
            "background": (30, 30, 50),
            "title": (255, 255, 255),
            "text": (230, 230, 230),
            "button_bg": (100, 100, 100),
            "button_hover_bg": (150, 150, 150),
            "scroll_bg": (40, 40, 60)  # Color para el contenedor de scroll
        }

        # Configuración del botón volver
        self.button_width = 200
        self.button_height = 50
        self.button_margin = 20
        self.back_button_rect = pygame.Rect(
            self.button_margin, 
            self.button_margin, 
            self.button_width, 
            self.button_height
        )

        # Configuración del contenedor de texto
        self.content_margin = 100
        self.scroll_position = 0
        self.scroll_speed = 30
        self.line_spacing = 40
        
        # Calcular dimensiones del contenedor
        self.container_rect = pygame.Rect(
            self.content_margin,
            150,  # Margen superior para dejar espacio al título
            self.screen.get_width() - (self.content_margin * 2),
            self.screen.get_height() - 200  # Margen inferior
        )

    def draw(self):
        self.screen.fill(self.colors["background"])

        # Título centrado
        title_surface = self.font_title.render(self.model.title, True, self.colors["title"])
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title_surface, title_rect)

        # Crear superficie para el contenido con scroll
        content_height = len(self.model.credits_text) * self.line_spacing
        content_surface = pygame.Surface((
            self.container_rect.width,
            max(content_height, self.container_rect.height)
        ))
        content_surface.fill(self.colors["background"])

        # Renderizar texto en la superficie de contenido
        for i, line in enumerate(self.model.credits_text):
            text_surface = self.font_text.render(line, True, self.colors["text"])
            text_rect = text_surface.get_rect(
                centerx=content_surface.get_width() // 2,
                top=i * self.line_spacing
            )
            content_surface.blit(text_surface, text_rect)

        # Crear máscara para el contenedor
        self.screen.set_clip(self.container_rect)
        
        # Dibujar el contenido con scroll
        self.screen.blit(
            content_surface,
            self.container_rect.move(0, -self.scroll_position)
        )
        
        # Restablecer máscara
        self.screen.set_clip(None)

        # Botón Volver con efecto hover
        mouse_pos = pygame.mouse.get_pos()
        bg_color = (
            self.colors["button_hover_bg"] 
            if self.back_button_rect.collidepoint(mouse_pos) 
            else self.colors["button_bg"]
        )

        pygame.draw.rect(
            self.screen, 
            bg_color, 
            self.back_button_rect, 
            border_radius=10
        )

        back_text = self.font_back.render("Volver", True, self.colors["text"])
        back_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_rect)

        pygame.display.flip()

    def handle_event(self, event):
        """Maneja eventos de mouse y teclado."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo
                if self.back_button_rect.collidepoint(event.pos):
                    return True
            elif event.button == 4:  # Scroll hacia arriba
                self.scroll_position = max(0, self.scroll_position - self.scroll_speed)
            elif event.button == 5:  # Scroll hacia abajo
                max_scroll = len(self.model.credits_text) * self.line_spacing - self.container_rect.height
                self.scroll_position = min(max_scroll, self.scroll_position + self.scroll_speed)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_position = max(0, self.scroll_position - self.scroll_speed)
            elif event.key == pygame.K_DOWN:
                max_scroll = len(self.model.credits_text) * self.line_spacing - self.container_rect.height
                self.scroll_position = min(max_scroll, self.scroll_position + self.scroll_speed)
        return False