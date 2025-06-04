"""Sistema de enemigos del juego.

Contiene la clase base Enemy que maneja todos los tipos de enemigos según su nivel.
"""
from dataclasses import dataclass, field
from models.entity import Entity
from services.config import CONFIG
from math import atan2, cos, sin, floor, ceil, sqrt
from models.hitbox import Hitbox
import time

@dataclass
class Enemy(Entity):
    """Clase base para todos los enemigos.
    """
    speed: float = 5.0
    damage: float = 10.0
    attack_range: float = 1.0
    attack_cooldown: float = 1.0
    level: int = 1
    _current_cooldown: float = 0.0
    _knockback_active: bool = field(default=False, init=False, repr=False)
    _knockback_start_time: float = field(default=0.0, init=False, repr=False)
    _knockback_direction: tuple[float, float] = field(default=(0.0, 0.0), init=False, repr=False)
    _knockback_force: float = field(default=0.0, init=False, repr=False)
    _knockback_velocity: tuple[float, float] = field(default=(0.0, 0.0), init=False, repr=False)

    def __init__(self, x: float, y: float, level: int):
        """Inicializa un enemigo con estadísticas basadas en su nivel."""
        enemy_types = {
            1: 'level_1',
            2: 'level_2',
            3: 'level_3',
            4: 'level_4',
            5: 'level_5'
        }
        
        enemy_type = enemy_types[level]
        super().__init__(x=x, y=y)
        
        # Configurar estadísticas según el nivel
        self.speed = CONFIG['enemies'][enemy_type]['speed']
        self.damage = CONFIG['enemies'][enemy_type]['damage']
        self.level = level

    def update(self, dt: float, player, map_obj):
        """Actualiza el estado del enemigo."""
        if not self.is_alive:
            return
            
        # Actualizar cooldown de ataque
        if self._current_cooldown > 0:
            self._current_cooldown -= dt
            
        # Actualizar knockback si está activo
        if self._knockback_active:
            self._update_knockback(dt, map_obj)
        else:
            # Movimiento normal hacia el jugador
            self._move_towards_player(dt, player, map_obj)
            
        # Intentar atacar si está en rango
        if self._can_attack(player):
            self._attack(player)
            
    def _update_knockback(self, dt: float, map_obj):
        """Actualiza el estado del knockback."""
        current_time = time.time()
        elapsed_time = current_time - self._knockback_start_time
        
        if elapsed_time >= CONFIG['knockback']['duration']:
            self._knockback_active = False
            self._knockback_velocity = (0.0, 0.0)
            return
            
        # Calcular la velocidad actual con fricción
        friction = CONFIG['knockback']['friction']
        vx = self._knockback_velocity[0] * friction
        vy = self._knockback_velocity[1] * friction
        
        # Calcular nueva posición
        new_x = self.x + vx * dt
        new_y = self.y + vy * dt
        
        # Verificar colisiones con el mapa
        if self._can_move_to(new_x, self.y, map_obj):
            self.x = new_x
        else:
            vx = 0
            
        if self._can_move_to(self.x, new_y, map_obj):
            self.y = new_y
        else:
            vy = 0
            
        # Actualizar velocidad
        self._knockback_velocity = (vx, vy)
            
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
        if self._current_cooldown > 0 or self._knockback_active:
            return False
            
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2)**0.5
        
        return distance <= self.attack_range
        
    def _attack(self, player):
        """Realiza un ataque al jugador."""
        player.take_damage(self.damage)
        self._current_cooldown = self.attack_cooldown
        
    def check_attack_hit(self, attack) -> bool:
        """Verifica si el enemigo está dentro del rango de un ataque."""
        if not attack.is_executing:
            return False
            
        # Calcular el centro del enemigo
        center_x = self.x + (self.width / 2)
        center_y = self.y + (self.height / 2)
        
        # Verificar si está en rango
        if attack.is_in_range(center_x, center_y):
            # Calcular daño
            damage = attack.calculate_damage()
            self.take_damage(damage)
            
            # Calcular dirección del knockback (opuesta a la dirección del enemigo hacia el jugador)
            dx = center_x - attack._source_x
            dy = center_y - attack._source_y
            
            # Normalizar el vector
            length = sqrt(dx*dx + dy*dy)
            if length > 0:
                knockback_dir = (dx/length, dy/length)
                
                # Iniciar knockback
                self._knockback_active = True
                self._knockback_start_time = time.time()
                self._knockback_direction = knockback_dir
                self._knockback_force = attack.knockback
                
                # Calcular velocidad inicial
                initial_speed = self._knockback_force * 2  # Factor de velocidad inicial
                self._knockback_velocity = (
                    knockback_dir[0] * initial_speed,
                    knockback_dir[1] * initial_speed
                )
                
            return True
            
        return False