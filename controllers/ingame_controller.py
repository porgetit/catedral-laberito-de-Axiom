"""Controlador de la escena de juego en curso.

Maneja entrada WASD + ratón y actualiza el modelo Player + Map.

TODO: El sistema de ataques necesita ser corregido:
- La dirección del ataque no apunta correctamente hacia el cursor
- El knockback no se aplica en la dirección correcta
- Los rangos de los ataques no funcionan como se espera
"""
import pygame
from models.player import Player
from models.map_grid import MapGrid
from models.enemies import BasicEnemy, FastEnemy, HeavyEnemy, RangedEnemy, BossEnemy
from views.ingame_view import InGameView
from services.config import CONFIG
import time
from math import atan2, cos, sin, sqrt

TILE_SIZE = CONFIG['map']['tile_size']

class InGameController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.map = MapGrid(CONFIG['map']['width'], CONFIG['map']['height'])
        self.player = Player(x=1, y=1)
        self.enemies = []
        self.view = InGameView(screen, self.map, self.player, self.enemies)
        
        # Estado del juego
        self.is_paused = False
        self.game_time = 0.0
        self.last_update_time = time.time()
        
        # Solo crear el jugador y enemigos si no estamos en modo debug del mapa
        if not CONFIG['debug']['map_only']:
            self._spawn_enemies()

    def _spawn_enemies(self):
        """Genera los enemigos iniciales."""
        # Enemigos básicos
        for _ in range(5):
            x, y = self.map.get_random_floor_position()
            self.enemies.append(BasicEnemy(x, y))
        
        # Enemigos rápidos
        for _ in range(3):
            x, y = self.map.get_random_floor_position()
            self.enemies.append(FastEnemy(x, y))
        
        # Enemigos pesados
        for _ in range(2):
            x, y = self.map.get_random_floor_position()
            self.enemies.append(HeavyEnemy(x, y))
        
        # Enemigos a distancia
        for _ in range(2):
            x, y = self.map.get_random_floor_position()
            self.enemies.append(RangedEnemy(x, y))
        
        # Jefe
        x, y = self.map.get_random_floor_position()
        self.enemies.append(BossEnemy(x, y))

    # Entrada
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_paused = not self.is_paused
                if self.is_paused:
                    self.last_update_time = time.time()
                return
                
        if not self.is_paused and not CONFIG['debug']['map_only']:
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self._handle_movement(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_attack(event.button)

    def _handle_movement(self, event: pygame.event.Event):
        """Maneja el movimiento del jugador."""
        is_key_down = event.type == pygame.KEYDOWN
        
        if event.key == pygame.K_w:
            self.player.move_up = is_key_down
        elif event.key == pygame.K_s:
            self.player.move_down = is_key_down
        elif event.key == pygame.K_a:
            self.player.move_left = is_key_down
        elif event.key == pygame.K_d:
            self.player.move_right = is_key_down

    def _handle_attack(self, button):
        """Maneja los ataques del jugador."""
        # Obtener posición del mouse en coordenadas de pantalla
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Convertir coordenadas de pantalla a coordenadas del juego
        # Primero ajustamos por los márgenes
        mouse_x -= CONFIG['game_area']['margins']['left']
        mouse_y -= CONFIG['game_area']['margins']['top']
        
        # Luego convertimos a coordenadas del juego
        game_x = mouse_x / TILE_SIZE
        game_y = mouse_y / TILE_SIZE
        
        # Calcular dirección del ataque desde el centro del jugador
        player_center_x = self.player.x + (self.player.width / 2)
        player_center_y = self.player.y + (self.player.height / 2)
        
        dx = game_x - player_center_x
        dy = game_y - player_center_y
        
        # Normalizar el vector de dirección
        length = sqrt(dx*dx + dy*dy)
        if length > 0:
            direction = (dx/length, dy/length)
        else:
            direction = (0, 0)
        
        # Encontrar el enemigo más cercano en el rango
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in self.enemies:
            if enemy.is_alive:
                # Calcular distancia desde el centro del jugador al centro del enemigo
                enemy_center_x = enemy.x + (enemy.width / 2)
                enemy_center_y = enemy.y + (enemy.height / 2)
                
                dx = enemy_center_x - player_center_x
                dy = enemy_center_y - player_center_y
                distance = sqrt(dx*dx + dy*dy) * TILE_SIZE  # Convertir a píxeles
                
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
        
        # Ejecutar el ataque correspondiente
        if button == 1:  # Click izquierdo
            if closest_enemy and min_distance <= self.player._uppercut.range_px:
                self.player.cast_uppercut(closest_enemy, direction)
        elif button == 3:  # Click derecho
            if closest_enemy and min_distance <= self.player._explosion.range_px:
                self.player.cast_point_blank_explosion(closest_enemy, direction)

    def update(self, dt: float):
        """Actualiza el estado del juego."""
        if not self.is_paused:
            # Actualizar tiempo de juego
            current_time = time.time()
            self.game_time += current_time - self.last_update_time
            self.last_update_time = current_time
            
            if not CONFIG['debug']['map_only']:
                # Actualizar jugador
                self.player.update(dt, self.map)
                
                # Actualizar enemigos
                for enemy in self.enemies:
                    if enemy.is_alive:
                        enemy.update(dt, self.player, self.map)
                
                # Actualizar ataques del jugador
                self.player._uppercut.update(dt)
                self.player._explosion.update(dt)

    def render(self):
        self.view.draw(
            self.is_paused,
            self.game_time
        )
