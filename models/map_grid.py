"""Modelo del mapa del juego.

Implementa una cuadrícula lógica para el mapa con paredes y suelos.
"""
from dataclasses import dataclass
from models.hitbox import Hitbox
from services.config import CONFIG
import random

@dataclass
class MapGrid:
    """Cuadrícula lógica del mapa."""
    width: int = CONFIG['map']['width']
    height: int = CONFIG['map']['height']
    grid: list[list[bool]] = None  # True = pared, False = suelo
    
    def __post_init__(self):
        """Inicializa la cuadrícula del mapa."""
        self.grid = [[True for _ in range(self.width)] for _ in range(self.height)]
        self._generate_map()
        
    def _generate_map(self):
        """Genera un mapa simple con paredes solo en los bordes."""
        # Hacer todo el mapa suelo
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = False
                
        # Añadir paredes en los bordes
        for x in range(self.width):
            self.grid[0][x] = True  # Pared superior
            self.grid[self.height-1][x] = True  # Pared inferior
            
        for y in range(self.height):
            self.grid[y][0] = True  # Pared izquierda
            self.grid[y][self.width-1] = True  # Pared derecha
            
    def is_walkable(self, x: int, y: int) -> bool:
        """Verifica si una posición es transitable."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return not self.grid[y][x]
        
    def get_wall_hitbox(self, x: int, y: int) -> Hitbox:
        """Obtiene la hitbox de una pared en la posición dada."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return None
        if not self.grid[y][x]:
            return None
        return Hitbox(x, y, 1, 1)
        
    def get_random_floor_position(self) -> tuple[int, int]:
        """Obtiene una posición aleatoria de suelo."""
        while True:
            x = random.randint(1, self.width-2)
            y = random.randint(1, self.height-2)
            if self.is_walkable(x, y):
                return (x, y)