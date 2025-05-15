"""Pruebas unitarias de los ataques del jugador."""
import pytest
from models.player import Player
from models.entity import Entity
from models.map_grid import MapGrid
from services.config import CONFIG
import time

class MockEntity(Entity):
    """Entidad de prueba para los ataques del jugador."""
    def __init__(self, x=0, y=0):
        super().__init__(x=x, y=y)
        self.damage_taken = 0
        self.knockback_applied = False
        
    def take_damage(self, damage: float):
        self.damage_taken += damage
        super().take_damage(damage)
        
    def apply_knockback(self, force: float, source_x: float = None, source_y: float = None):
        self.knockback_applied = True
        super().apply_knockback(force, source_x, source_y)

def test_player_uppercut_cooldown():
    """Prueba el sistema de cooldown del Golpe Ascendente."""
    player = Player(x=0, y=0)
    target = MockEntity(x=5, y=0)
    map_obj = MapGrid(10, 10)
    
    # Primer ataque
    player.cast_uppercut(target)
    assert target.damage_taken == CONFIG['player']['physical_damage']
    assert player._uppercut_cooldown > 0
    
    # Intentar atacar durante el cooldown
    target.damage_taken = 0
    player.cast_uppercut(target)
    assert target.damage_taken == 0  # No debería aplicar daño
    
    # Esperar el cooldown
    player.update(player._uppercut.cooldown, map_obj)
    assert player._uppercut_cooldown <= 0
    
    # Segundo ataque después del cooldown
    player.cast_uppercut(target)
    assert target.damage_taken == CONFIG['player']['physical_damage']

def test_player_explosion_mp_cost():
    """Prueba el costo de MP de la Explosión a Quemarropa."""
    player = Player(x=0, y=0)
    target = MockEntity(x=5, y=0)
    map_obj = MapGrid(10, 10)
    initial_mp = player.mp
    
    # Primer ataque
    player.cast_point_blank_explosion(target)
    assert target.damage_taken == CONFIG['player']['magical_damage']
    assert player.mp == initial_mp - CONFIG['attacks']['melee']['point_blank_explosion']['mp_cost']
    
    # Intentar atacar sin MP suficiente
    player.mp = 0
    target.damage_taken = 0
    player.cast_point_blank_explosion(target)
    assert target.damage_taken == 0  # No debería aplicar daño

def test_player_attack_direction():
    """Prueba la dirección de los ataques del jugador."""
    player = Player(x=0, y=0)
    target = MockEntity(x=5, y=0)
    map_obj = MapGrid(10, 10)
    
    # Probar diferentes direcciones
    directions = [
        (1, 0),   # Derecha
        (-1, 0),  # Izquierda
        (0, 1),   # Abajo
        (0, -1),  # Arriba
        (1, 1),   # Diagonal
    ]
    
    for direction in directions:
        # Resetear cooldowns
        player._uppercut_cooldown = 0
        player._explosion_cooldown = 0
        
        # Probar Golpe Ascendente
        player.cast_uppercut(target, direction)
        assert player._uppercut.direction == direction
        
        # Probar Explosión a Quemarropa
        player.cast_point_blank_explosion(target, direction)
        assert player._explosion.direction == direction

def test_player_attack_execution_time():
    """Prueba el tiempo de ejecución de los ataques del jugador."""
    player = Player(x=0, y=0)
    map_obj = MapGrid(10, 10)
    
    # Probar Golpe Ascendente
    player.cast_uppercut()
    assert player._uppercut.is_executing
    
    # Simular paso del tiempo
    player.update(player._uppercut.cast_time, map_obj)
    assert not player._uppercut.is_executing
    
    # Probar Explosión a Quemarropa
    player.cast_point_blank_explosion()
    assert player._explosion.is_executing
    
    # Simular paso del tiempo
    player.update(player._explosion.cast_time, map_obj)
    assert not player._explosion.is_executing

def test_player_attack_knockback():
    """Prueba el sistema de knockback de los ataques."""
    player = Player(x=0, y=0)
    target = MockEntity(x=5, y=0)
    map_obj = MapGrid(10, 10)
    
    # Probar knockback del Golpe Ascendente
    player.cast_uppercut(target)
    assert target.knockback_applied
    
    # Resetear estado
    target.knockback_applied = False
    
    # Probar knockback de la Explosión a Quemarropa
    player.cast_point_blank_explosion(target)
    assert target.knockback_applied 