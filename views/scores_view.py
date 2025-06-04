import pygame
from models.scores import ScoresModel

class ScoresView:
    def __init__(self, screen, model: ScoresModel): # Tipado para claridad
        self.screen = screen
        self.model = model
        pygame.font.init() # Asegurarse que pygame.font está inicializado
        self.font_title = pygame.font.Font(None, 74)
        self.font_scores = pygame.font.Font(None, 36)
        self.font_back = pygame.font.Font(None, 50)

        self.colors = {
            "background": (30, 30, 50),
            "title": (255, 255, 255),
            "text": (230, 230, 230),
            "highlight": (255, 215, 0),  # Color dorado para el mejor puntaje
            "button_bg": (100, 100, 100),
            "button_hover_bg": (150, 150, 150)
        }

        self.back_button_rect = None

    def draw(self):
        self.screen.fill(self.colors["background"])

        # Título
        title_surface = self.font_title.render(self.model.title, True, self.colors["title"])
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_surface, title_rect)

        # Puntajes - Forzar actualización cada vez que se dibuja
        scores = self.model.get_top_scores(force_refresh=True)
        start_y = 200
        spacing = 40

        if not scores:
            # Mostrar mensaje si no hay puntajes
            no_scores_text = "No hay puntajes registrados"
            no_scores_surface = self.font_scores.render(no_scores_text, True, self.colors["text"])
            no_scores_rect = no_scores_surface.get_rect(center=(self.screen.get_width() // 2, start_y))
            self.screen.blit(no_scores_surface, no_scores_rect)
        else:
            # Mostrar puntajes
            for i, (date, score) in enumerate(scores):
                # Formato de posición
                position = f"#{i + 1}"
                # Formato de fecha más corto (YYYY-MM-DD)
                date_str = date.split()[0]

                # Texto completo
                text = f"{position:>3} - {date_str:>10} - {score:>5} puntos"

                # Color según posición
                color = self.colors["highlight"] if i == 0 else self.colors["text"]

                score_surface = self.font_scores.render(text, True, color)
                score_rect = score_surface.get_rect(center=(self.screen.get_width() // 2, start_y + i * spacing))
                self.screen.blit(score_surface, score_rect)

        # Botón Volver
        button_width = 200
        button_height = 50
        button_x = (self.screen.get_width() - button_width) // 2
        button_y = self.screen.get_height() - 100

        self.back_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # Efecto hover
        mouse_pos = pygame.mouse.get_pos()
        bg_color = self.colors["button_hover_bg"] if self.back_button_rect.collidepoint(mouse_pos) else self.colors["button_bg"]

        pygame.draw.rect(self.screen, bg_color, self.back_button_rect, border_radius=10)

        back_text = self.font_back.render("Volver", True, self.colors["text"])
        back_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_rect)

        pygame.display.flip()

    def handle_event(self, event):
        """
        Maneja eventos, por ejemplo, clic en el botón "Volver".
        Devuelve True si el botón fue presionado, False en caso contrario.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Botón izquierdo del ratón
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos):
                    print("Botón Volver presionado")
                    return True # Indicar que se debe volver
        return False