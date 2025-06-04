"""Controlador raíz que orquesta la aplicación."""
import pygame
from controllers.ingame_controller import InGameController
from controllers.menu_controller import MenuController
from models.menu import MenuModel
from models.scores import ScoresModel
from models.credits import CreditsModel
from views.menu_view import MenuView
from views.scores_view import ScoresView
from views.credits_view import CreditsView
from services.records import RecordsService
from services.audio_manager import AudioManager

class AppController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        # Crear una única instancia de RecordsService para toda la app
        self.records_service = RecordsService()
        
        # Inicializar el AudioManager
        self.audio_manager = AudioManager()
        
        # Crear componentes del menú
        self.menu_model = MenuModel()
        self.menu_view = MenuView(screen, self.menu_model)
        self.menu_controller = MenuController(self.menu_model)
        
        # Crear componentes de puntajes usando el mismo RecordsService
        self.scores_model = ScoresModel(self.records_service)
        self.scores_view = ScoresView(screen, self.scores_model)
        
        # Crear componentes de créditos
        self.credits_model = CreditsModel()
        self.credits_view = CreditsView(screen, self.credits_model)
        
        # Iniciar con el menú
        self.current_scene = "menu"
        self.ingame_controller = None
        
        # Reproducir música del menú al inicio
        self.audio_manager.play_menu_music()

    def handle_event(self, event: pygame.event.Event):
        if self.current_scene == "menu":
            action = self.menu_controller.handle_event(event, self.menu_view.get_button_rects())
            if action == "Jugar":
                self.current_scene = "game"
                self.ingame_controller = InGameController(self.screen)
                self.audio_manager.play_coliseo_music()
            elif action == "Puntajes":
                self.current_scene = "scores"
            elif action == "Créditos":
                self.current_scene = "credits"
            elif action == "Salir":
                return False
        elif self.current_scene == "game":
            result = self.ingame_controller.handle_event(event)
            if result == "menu":
                self.current_scene = "menu"
                self.audio_manager.play_menu_music()
        elif self.current_scene == "scores":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.scores_view.back_button_rect.collidepoint(event.pos):
                    self.current_scene = "menu"
        elif self.current_scene == "credits":
            # Manejar todos los eventos de la vista de créditos
            if self.credits_view.handle_event(event):
                self.current_scene = "menu"
        return True

    def update(self, dt: float):
        if self.current_scene == "game":
            self.ingame_controller.update(dt)

    def render(self):
        if self.current_scene == "menu":
            self.menu_view.draw()
        elif self.current_scene == "game":
            self.ingame_controller.render()
        elif self.current_scene == "scores":
            self.scores_view.draw()
        elif self.current_scene == "credits":
            self.credits_view.draw()
        pygame.display.flip()
