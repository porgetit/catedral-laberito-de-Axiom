"""Pruebas unitarias del sistema de ataques.
"""
import pytest
from models.attacks import Attack, Uppercut, PointBlankExplosion
from models.entity import Entity
from services.config import CONFIG
import time

class MockEntity(Entity):
    """Entidad de prueba para los ataques."""
    def __init__(self, x=0, y=0):
        super().__init__(x=x, y=y)
        self.damage_taken = 0
        self.knockback_applied = False
        self.knockback_direction = (0, 0)
        
    def take_damage(self, damage: float):
        self.damage_taken += damage
        super().take_damage(damage)
        
    def apply_knockback(self, force: float, source_x: float = None, source_y: float = None):
        self.knockback_applied = True
        if source_x is not None and source_y is not None:
            self.knockback_direction = (self.x - source_x, self.y - source_y)
        super().apply_knockback(force, source_x, source_y)

def test_attack_execution():
    """Prueba la ejecución básica de un ataque."""
    # Crear un ataque de prueba
    attack = Attack(
        name="Test Attack",
        damage=10.0,
        range_px=50.0,
        cast_time=0.25,
        cooldown=1.0,
        mp_cost=5.0,
        knockback=10.0,
        critical_multiplier=1.5
    )
    
    # Crear un objetivo de prueba
    target = MockEntity(x=5, y=5)
    
    # Ejecutar el ataque
    attack.execute(target, direction=(1, 0))
    
    # Verificar que el daño se aplicó
    assert target.damage_taken == 10.0
    assert target.knockback_applied
    assert attack.is_executing
    assert attack.direction == (1, 0)

def test_attack_critical_hit():
    """Prueba el sistema de golpes críticos."""
    # Crear un ataque con alta probabilidad de crítico
    CONFIG['player']['critical_chance'] = 1.0  # Forzar crítico
    attack = Attack(
        name="Critical Test",
        damage=10.0,
        range_px=50.0,
        cast_time=0.25,
        cooldown=1.0,
        mp_cost=5.0,
        knockback=10.0,
        critical_multiplier=2.0
    )
    
    target = MockEntity()
    attack.execute(target)
    
    # Verificar que el daño crítico se aplicó
    assert target.damage_taken == 20.0  # 10.0 * 2.0

def test_uppercut_initialization():
    """Prueba la inicialización del Golpe Ascendente."""
    uppercut = Uppercut()
    config = CONFIG['attacks']['melee']['uppercut']
    
    assert uppercut.name == config['name']
    assert uppercut.damage == CONFIG['player']['physical_damage']
    assert uppercut.range_px == config['range_px']
    assert uppercut.cast_time == config['cast_time']
    assert uppercut.cooldown == config['cooldown']
    assert uppercut.knockback == config['knockback']
    assert uppercut.mp_cost == config['mp_cost']

def test_point_blank_explosion_initialization():
    """Prueba la inicialización de la Explosión a Quemarropa."""
    explosion = PointBlankExplosion()
    config = CONFIG['attacks']['melee']['point_blank_explosion']
    
    assert explosion.name == config['name']
    assert explosion.damage == CONFIG['player']['magical_damage']
    assert explosion.range_px == config['range_px']
    assert explosion.cast_time == config['cast_time']
    assert explosion.cooldown == config['cooldown']
    assert explosion.knockback == config['knockback']
    assert explosion.mp_cost == config['mp_cost']

def test_attack_execution_time():
    """Prueba el tiempo de ejecución de un ataque."""
    attack = Attack(
        name="Timing Test",
        damage=10.0,
        range_px=50.0,
        cast_time=0.25,
        cooldown=1.0,
        mp_cost=5.0,
        knockback=10.0,
        critical_multiplier=1.5
    )
    
    # Ejecutar el ataque
    attack.execute(None)
    assert attack.is_executing
    
    # Simular paso del tiempo
    attack.update(0.2)  # Menos que cast_time
    assert attack.is_executing
    
    # Simular el tiempo restante
    attack.update(0.1)  # Total 0.3 > cast_time
    assert not attack.is_executing

def test_attack_direction():
    """Prueba el sistema de dirección de ataques."""
    attack = Attack(
        name="Direction Test",
        damage=10.0,
        range_px=50.0,
        cast_time=0.25,
        cooldown=1.0,
        mp_cost=5.0,
        knockback=10.0,
        critical_multiplier=1.5
    )
    
    # Probar diferentes direcciones
    directions = [
        (1, 0),   # Derecha
        (-1, 0),  # Izquierda
        (0, 1),   # Abajo
        (0, -1),  # Arriba
        (1, 1),   # Diagonal
        (0, 0)    # Sin dirección
    ]
    
    for direction in directions:
        attack.execute(None, direction)
        assert attack.direction == direction 