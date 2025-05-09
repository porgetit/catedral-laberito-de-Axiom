
"""Controlador de la escena de juego en curso.

Maneja entrada WASD + ratón y actualiza el modelo Player + Map.
"""
import pygame
from models.player import Player
from models.map_grid import MapGrid
from views.ingame_view import InGameView

class InGameController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.map = MapGrid(64, 64)  # Mapa base de 64x64 celdas
        self.player = Player(x=32, y=32)  # Centro aproximado
        self.view = InGameView(screen, self.map, self.player)

    # Entrada
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self._handle_keyboard(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.player.cast_melee_burst()

    def _handle_keyboard(self, event: pygame.event.Event):
        pressed = event.type == pygame.KEYDOWN
        if event.key == pygame.K_w:
            self.player.move_up = pressed
        elif event.key == pygame.K_s:
            self.player.move_down = pressed
        elif event.key == pygame.K_a:
            self.player.move_left = pressed
        elif event.key == pygame.K_d:
            self.player.move_right = pressed

    def update(self, dt: float):
        self.player.update(dt, self.map)

    def render(self):
        self.view.draw()
