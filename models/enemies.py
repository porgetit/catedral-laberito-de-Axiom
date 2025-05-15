"""Sistema de enemigos del juego.

Contiene la clase base Enemy y sus implementaciones concretas.
"""
from dataclasses import dataclass
from models.entity import Entity
from services.config import CONFIG
from math import atan2, cos, sin, floor, ceil
from models.hitbox import Hitbox

@dataclass
class Enemy(Entity):
    """Clase base para todos los enemigos."""
    speed: float = 5.0
    damage: float = 10.0
    attack_range: float = 1.0
    attack_cooldown: float = 1.0
    _current_cooldown: float = 0.0
    
    def update(self, dt: float, player, map_obj):
        """Actualiza el estado del enemigo."""
        if not self.is_alive:
            return
            
        # Actualizar cooldown de ataque
        if self._current_cooldown > 0:
            self._current_cooldown -= dt
            
        # Movimiento hacia el jugador
        self._move_towards_player(dt, player, map_obj)
        
        # Intentar atacar si está en rango
        if self._can_attack(player):
            self._attack(player)
            
    def _move_towards_player(self, dt: float, player, map_obj):
        """Mueve al enemigo hacia el jugador."""
        dx = player.x - self.x
        dy = player.y - self.y
        
        if dx != 0 or dy != 0:
            # Calcular la distancia
            distance = (dx**2 + dy**2)**0.5
            # Normalizar y calcular movimiento propuesto
            new_x = self.x + (dx/distance) * self.speed * dt
            new_y = self.y + (dy/distance) * self.speed * dt
            
            # Intentar movimiento en X
            if dx != 0 and self._can_move_to(new_x, self.y, map_obj):
                self.x = new_x
                
            # Intentar movimiento en Y
            if dy != 0 and self._can_move_to(self.x, new_y, map_obj):
                self.y = new_y
                
    def _can_move_to(self, new_x: float, new_y: float, map_obj) -> bool:
        """Verifica si el enemigo puede moverse a la nueva posición."""
        enemy_hitbox = Hitbox(new_x, new_y, self.width, self.height)
        min_x = floor(new_x)
        max_x = ceil(new_x + self.width - 1e-6)
        min_y = floor(new_y)
        max_y = ceil(new_y + self.height - 1e-6)
        
        try:
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    wall_hitbox = map_obj.get_wall_hitbox(x, y)
                    if wall_hitbox and enemy_hitbox.collides_with(wall_hitbox):
                        return False
        except IndexError:
            return False
        return True
        
    def _can_attack(self, player) -> bool:
        """Verifica si el enemigo puede atacar al jugador."""
        if self._current_cooldown > 0:
            return False
            
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2)**0.5
        
        return distance <= self.attack_range
        
    def _attack(self, player):
        """Realiza un ataque al jugador."""
        player.take_damage(self.damage)
        self._current_cooldown = self.attack_cooldown

class BasicEnemy(Enemy):
    """Enemigo básico con estadísticas estándar."""
    
    def __init__(self, x: float, y: float):
        super().__init__(
            x=x,
            y=y,
            hp=50,
            speed=5.0,
            damage=10.0,
            attack_range=1.0,
            attack_cooldown=1.0
        )

class FastEnemy(Enemy):
    """Enemigo rápido con menos vida y daño."""
    
    def __init__(self, x: float, y: float):
        super().__init__(
            x=x,
            y=y,
            hp=30,
            speed=8.0,
            damage=5.0,
            attack_range=1.0,
            attack_cooldown=0.7
        )

class HeavyEnemy(Enemy):
    """Enemigo lento pero resistente y con más daño."""
    
    def __init__(self, x: float, y: float):
        super().__init__(
            x=x,
            y=y,
            hp=100,
            speed=3.0,
            damage=20.0,
            attack_range=1.2,
            attack_cooldown=1.5
        )

class RangedEnemy(Enemy):
    """Enemigo a distancia con menos vida pero ataque a rango."""
    
    def __init__(self, x: float, y: float):
        super().__init__(
            x=x,
            y=y,
            hp=40,
            speed=4.0,
            damage=8.0,
            attack_range=3.0,
            attack_cooldown=1.2
        )

class BossEnemy(Enemy):
    """Enemigo jefe con estadísticas elevadas."""
    
    def __init__(self, x: float, y: float):
        super().__init__(
            x=x,
            y=y,
            hp=200,
            speed=4.0,
            damage=25.0,
            attack_range=1.5,
            attack_cooldown=1.0
        ) 