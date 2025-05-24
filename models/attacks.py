"""Sistema de ataques del juego.

Contiene la clase base Attack y sus implementaciones concretas.
"""
from dataclasses import dataclass
from services.config import CONFIG
import random
import time
from math import sqrt

@dataclass
class Attack:
    """Clase base abstracta para todos los ataques."""
    name: str
    damage: float
    range: float  # Rango en unidades lógicas del juego
    cast_time: float
    cooldown: float
    mp_cost: float
    knockback: float
    critical_multiplier: float
    _is_executing: bool = False
    _start_time: float = 0
    _direction: tuple[float, float] = (0, 0)
    _source_x: float = 0
    _source_y: float = 0
    
    def execute(self, source_x: float, source_y: float, direction: tuple[float, float] = None):
        """Ejecuta el ataque desde una posición fuente."""
        # Guardar posición fuente y dirección
        self._source_x = source_x
        self._source_y = source_y
        self._direction = direction or (0, 0)
        self._is_executing = True
        self._start_time = time.time()
        
    def is_in_range(self, target_x: float, target_y: float) -> bool:
        """Verifica si un punto está dentro del rango del ataque."""
        dx = target_x - self._source_x
        dy = target_y - self._source_y
        distance = sqrt(dx*dx + dy*dy)
        return distance <= self.range
        
    def calculate_damage(self) -> float:
        """Calcula el daño del ataque, incluyendo probabilidad de crítico."""
        damage = self.damage
        if random.random() < CONFIG['player']['critical_chance']:
            damage *= self.critical_multiplier
        return damage
        
    def calculate_knockback_direction(self, target_x: float, target_y: float) -> tuple[float, float]:
        """Calcula la dirección del knockback desde el punto fuente al objetivo."""
        dx = target_x - self._source_x
        dy = target_y - self._source_y
        
        # Normalizar el vector
        length = sqrt(dx*dx + dy*dy)
        if length > 0:
            return (-dx/length, -dy/length)
        return (0, 0)
        
    def update(self, dt: float):
        """Actualiza el estado del ataque."""
        if self._is_executing:
            if time.time() - self._start_time >= self.cast_time:
                self._is_executing = False
                
    @property
    def is_executing(self) -> bool:
        """Indica si el ataque está en ejecución."""
        return self._is_executing
        
    @property
    def direction(self) -> tuple[float, float]:
        """Devuelve la dirección del ataque."""
        return self._direction

class Uppercut(Attack):
    """Ataque básico de golpe ascendente."""
    
    def __init__(self):
        config = CONFIG['attacks']['melee']['uppercut']
        super().__init__(
            name=config['name'],
            damage=CONFIG['player']['physical_damage'],
            range=config['range'],
            cast_time=config['cast_time'],
            cooldown=config['cooldown'],
            knockback=config['knockback'],
            mp_cost=config['mp_cost'],
            critical_multiplier=CONFIG['player']['critical_multiplier']
        )

class PointBlankExplosion(Attack):
    """Ataque mágico de explosión a quemarropa."""
    
    def __init__(self):
        config = CONFIG['attacks']['melee']['point_blank_explosion']
        super().__init__(
            name=config['name'],
            damage=CONFIG['player']['magical_damage'],
            range=config['range'],
            cast_time=config['cast_time'],
            cooldown=config['cooldown'],
            knockback=config['knockback'],
            mp_cost=config['mp_cost'],
            critical_multiplier=CONFIG['player']['critical_multiplier']
        )