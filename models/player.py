"""Modelo del jugador con movimiento y ataques básicos.
"""
from dataclasses import dataclass, field
from typing import Optional
from models.entity import Entity

MOVE_SPEED = 15  # píxeles por segundo
MELEE_COOLDOWN = 0.4  # segundos
MELEE_COST = 5  # MP

@dataclass
class Player(Entity):
    hp: int = 100
    mp: int = 50
    _melee_cooldown: float = field(default=0.0, init=False, repr=False)

    # Input flags
    move_up: bool = field(default=False, repr=False)
    move_down: bool = field(default=False, repr=False)
    move_left: bool = field(default=False, repr=False)
    move_right: bool = field(default=False, repr=False)

    def update(self, dt: float, map_obj):
        # Movimiento propuesto
        dx = (self.move_right - self.move_left) * MOVE_SPEED * dt
        dy = (self.move_down - self.move_up) * MOVE_SPEED * dt

        # Verificar colisiones antes de mover
        new_x = self.x + dx
        new_y = self.y + dy
        if map_obj.is_walkable(int(new_x), int(self.y)):  # Movimiento horizontal
            self.x = new_x
        if map_obj.is_walkable(int(self.x), int(new_y)):  # Movimiento vertical
            self.y = new_y

        # Enfriamiento del ataque
        if self._melee_cooldown > 0:
            self._melee_cooldown -= dt

    # Ataque cuerpo a cuerpo (explosión mágica)
    def cast_melee_burst(self):
        if self._melee_cooldown <= 0 and self.mp >= MELEE_COST:
            self.mp -= MELEE_COST
            self._melee_cooldown = MELEE_COOLDOWN
            # Generar un evento interno o simple print (placeholder)
            print("¡Explosión de fuego!")
