
"""Controlador raíz que orquesta la aplicación.

Gestiona el cambio de escenas y delega el loop a la escena activa.
"""
import pygame
from controllers.ingame_controller import InGameController

class AppController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.current_scene = InGameController(screen)

    # Delegar eventos a la escena
    def handle_event(self, event: pygame.event.Event):
        self.current_scene.handle_event(event)

    def update(self, dt: float):
        self.current_scene.update(dt)

    def render(self):
        self.current_scene.render()
        pygame.display.flip()
