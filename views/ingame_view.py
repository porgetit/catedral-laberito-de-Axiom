
"""Vista pasiva de la escena de juego.
"""
import pygame
TILE_SIZE = 10  # Factor de escala para mostrar 64×64 en ventana 640×640

COLORS = {
    'floor': (40, 40, 40),
    'wall': (90, 90, 90),
    'player': (200, 50, 50),
}

class InGameView:
    def __init__(self, screen: pygame.Surface, map_obj, player):
        self.screen = screen
        self.map = map_obj
        self.player = player

    def draw(self):
        # Dibujar mapa
        for y in range(self.map.height):
            for x in range(self.map.width):
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                color = COLORS['floor'] if self.map.is_walkable(x, y) else COLORS['wall']
                self.screen.fill(color, rect)
        # Dibujar jugador
        px = int(self.player.x * TILE_SIZE)
        py = int(self.player.y * TILE_SIZE)
        self.screen.fill(COLORS['player'],
                         pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))
