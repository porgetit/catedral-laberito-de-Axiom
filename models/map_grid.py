"""Mapa lógico en cuadrícula (64x64).

Solo contiene tipo de celda por ahora (0 = suelo, 1 = muro)
"""
class MapGrid:
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Borde de muros, interior suelo
        self.grid = [[1 if x in (0, width-1) or y in (0, height-1) else 0 for x in range(width)] for y in range(height)]
    
    def is_walkable(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] == 0
        return False  # Fuera de los límites no es transitable
