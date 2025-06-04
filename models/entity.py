"""Entidad base: sólo lógica, sin dependencias gráficas.
"""
from models.hitbox import Hitbox
from dataclasses import dataclass
from math import atan2, cos, sin

@dataclass
class Entity:
    x: float
    y: float
    width: float = 1
    height: float = 1
    hp: float = 100
    is_alive: bool = True
    
    def get_position(self) -> tuple[float, float]:
        """Devuelve la posición de la entidad."""
        return self.x, self.y

    @property
    def hitbox(self) -> Hitbox:
        """Devuelve la hitbox de la entidad."""
        return Hitbox(self.x, self.y, self.width, self.height)
        
    def take_damage(self, damage: float):
        """Recibe daño y actualiza el estado de la entidad."""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            
    def apply_knockback(self, force: float, source_x: float = None, source_y: float = None):
        """Aplica un knockback a la entidad desde una fuente."""
        if not self.is_alive:
            return
            
        # Si no se especifica la fuente, usar la posición actual
        if source_x is None:
            source_x = self.x
        if source_y is None:
            source_y = self.y
            
        # Calcular dirección del knockback
        dx = self.x - source_x
        dy = self.y - source_y
        
        # Normalizar y aplicar la fuerza
        if dx != 0 or dy != 0:
            angle = atan2(dy, dx)
            self.x += cos(angle) * force
            self.y += sin(angle) * force
