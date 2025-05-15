"""Pruebas unitarias del jugador."""
import pytest
from models.player import Player
from models.map_grid import MapGrid
from services.config import CONFIG

def test_player_movement():
    """Prueba el movimiento básico del jugador."""
    player = Player(x=1, y=1)
    map_obj = MapGrid(10, 10)
    
    # Probar movimiento hacia la derecha
    player.move_right = True
    player.update(1, map_obj)
    assert player.x > 1  # Debería moverse
    
    # Probar movimiento hacia la izquierda
    player.move_right = False
    player.move_left = True
    player.update(1, map_obj)
    assert player.x < 2  # Debería moverse hacia atrás

def test_player_collision():
    """Prueba las colisiones del jugador con paredes."""
    map_obj = MapGrid(10, 10)
    player = Player(x=1, y=1)
    
    # Intentar moverse hacia una pared
    player.move_right = True
    player.x = 8  # Cerca del borde del mapa
    player.update(1, map_obj)
    assert player.x < 9  # No debería atravesar la pared

def test_player_resources():
    """Prueba el sistema de recursos del jugador."""
    player = Player(x=0, y=0)
    
    # Verificar valores iniciales
    assert player.hp == CONFIG['player']['hp']
    assert player.mp == CONFIG['player']['mp']
    
    # Probar daño
    player.take_damage(10)
    assert player.hp == CONFIG['player']['hp'] - 10
    
    # Probar consumo de MP
    initial_mp = player.mp
    player.mp -= 20
    assert player.mp == initial_mp - 20
