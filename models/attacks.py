"""Sistema de ataques del juego.

Contiene la clase base Attack y sus implementaciones concretas.
"""
from dataclasses import dataclass
from services.config import CONFIG
import random
import time

@dataclass
class Attack:
    """Clase base abstracta para todos los ataques."""
    name: str
    damage: float
    range_px: float
    cast_time: float
    cooldown: float
    mp_cost: float
    knockback: float
    critical_multiplier: float
    _is_executing: bool = False
    _start_time: float = 0
    _direction: tuple[float, float] = (0, 0)
    
    def execute(self, target, direction: tuple[float, float] = None):
        """Ejecuta el ataque sobre un objetivo."""
        if target:
            # Aplicar daño base
            damage = self.damage
            # Aplicar probabilidad de golpe crítico
            if random.random() < CONFIG['player']['critical_chance']:
                damage *= self.critical_multiplier
            target.take_damage(damage)
            
            # Aplicar knockback en la dirección del ataque
            if direction:
                target.x += direction[0] * self.knockback
                target.y += direction[1] * self.knockback
            
        # Guardar dirección y tiempo de inicio
        self._direction = direction or (0, 0)
        self._is_executing = True
        self._start_time = time.time()
        
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
            range_px=config['range_px'],
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
            range_px=config['range_px'],
            cast_time=config['cast_time'],
            cooldown=config['cooldown'],
            knockback=config['knockback'],
            mp_cost=config['mp_cost'],
            critical_multiplier=CONFIG['player']['critical_multiplier']
        )