"""Modelo del jugador con movimiento y ataques básicos.
"""
from dataclasses import dataclass, field
from models.entity import Entity
from models.hitbox import Hitbox
from services.config import CONFIG
from models.attacks import Uppercut, PointBlankExplosion
from math import floor, ceil
import time

MOVE_SPEED = CONFIG['player']['speed']  # unidades por segundo

@dataclass
class Player(Entity):
    hp: int = CONFIG['player']['hp']
    mp: int = CONFIG['player']['mp']
    width: int = CONFIG['player']['width']
    height: int = CONFIG['player']['height']
    _uppercut_cooldown: float = field(default=0.0, init=False, repr=False)
    _explosion_cooldown: float = field(default=0.0, init=False, repr=False)
    _uppercut: Uppercut = field(default_factory=Uppercut, init=False, repr=False)
    _explosion: PointBlankExplosion = field(default_factory=PointBlankExplosion, init=False, repr=False)
    _last_regen_time: float = field(default_factory=time.time, init=False, repr=False)

    # Input flags
    move_up: bool = field(default=False, repr=False)
    move_down: bool = field(default=False, repr=False)
    move_left: bool = field(default=False, repr=False)
    move_right: bool = field(default=False, repr=False)

    def update(self, dt: float, map_obj):
        # Movimiento propuesto
        dx = (self.move_right - self.move_left) * MOVE_SPEED * dt
        dy = (self.move_down - self.move_up) * MOVE_SPEED * dt

        # Verificar colisiones por separado en X e Y
        new_x = self.x + dx
        new_y = self.y + dy

        # Intentar movimiento en X
        if dx != 0 and self._can_move_to(new_x, self.y, map_obj):
            self.x = new_x

        # Intentar movimiento en Y
        if dy != 0 and self._can_move_to(self.x, new_y, map_obj):
            self.y = new_y

        # Enfriamiento de los ataques
        if self._uppercut_cooldown > 0:
            self._uppercut_cooldown -= dt
        if self._explosion_cooldown > 0:
            self._explosion_cooldown -= dt

        # Regeneración de HP y MP
        current_time = time.time()
        if current_time - self._last_regen_time >= CONFIG['player']['time_to_regen']:
            # Regenerar HP
            if self.hp < CONFIG['player']['hp']:
                # Convertir el porcentaje a decimal (0.1% = 0.001)
                hp_regen_percent = CONFIG['player']['hp_regen'] / 100
                hp_regen = CONFIG['player']['hp'] * hp_regen_percent
                self.hp = min(self.hp + hp_regen, CONFIG['player']['hp'])
            
            # Regenerar MP
            if self.mp < CONFIG['player']['mp']:
                # Convertir el porcentaje a decimal (0.1% = 0.001)
                mp_regen_percent = CONFIG['player']['mp_regen'] / 100
                mp_regen = CONFIG['player']['mp'] * mp_regen_percent
                self.mp = min(self.mp + mp_regen, CONFIG['player']['mp'])
            
            self._last_regen_time = current_time
            
    def _can_move_to(self, new_x: float, new_y: float, map_obj) -> bool:
        """Verifica si la entidad puede moverse a la nueva posición."""
        player_hitbox = Hitbox(new_x, new_y, self.width, self.height)
        min_x = floor(new_x)
        max_x = ceil(new_x + self.width - 1e-6)
        min_y = floor(new_y)
        max_y = ceil(new_y + self.height - 1e-6)
        try:
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    wall_hitbox = map_obj.get_wall_hitbox(x, y)
                    if wall_hitbox and player_hitbox.collides_with(wall_hitbox):
                        return False
        except IndexError:
            return False
        return True
        
    def cast_uppercut(self, direction: tuple[float, float] = None):
        """Ejecuta el ataque de golpe ascendente."""
        if self._uppercut_cooldown <= 0:
            # Calcular el centro del jugador
            center_x = self.x + (self.width / 2)
            center_y = self.y + (self.height / 2)
            self._uppercut.execute(center_x, center_y, direction)
            self._uppercut_cooldown = self._uppercut.cooldown
            
    def cast_point_blank_explosion(self, direction: tuple[float, float] = None):
        """Ejecuta el ataque de explosión a quemarropa."""
        if self._explosion_cooldown <= 0 and self.mp >= self._explosion.mp_cost:
            # Calcular el centro del jugador
            center_x = self.x + (self.width / 2)
            center_y = self.y + (self.height / 2)
            self.mp -= self._explosion.mp_cost
            self._explosion.execute(center_x, center_y, direction)
            self._explosion_cooldown = self._explosion.cooldown
            