"""Prueba unitaria básica del modelo Player.
"""
from models.player import Player
from models.map_grid import MapGrid

def test_melee_cost():
    p = Player(20, 20)
    mp_inicial = p.mp
    p.cast_melee_burst()
    assert p.mp == mp_inicial - 5

def test_player_collision():
    map_obj = MapGrid(10, 10)
    p = Player(x=1, y=1)
    p.move_right = True
    p.update(1, map_obj)  # Movimiento hacia la derecha
    assert p.x == 2  # Movimiento permitido

    p.x = 8  # Cerca del muro derecho
    p.update(1, map_obj)
    assert p.x == 8  # No atraviesa el muro
