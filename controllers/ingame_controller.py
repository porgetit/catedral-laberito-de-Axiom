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
from services.records import RecordsService
import time
from math import atan2, cos, sin, sqrt, floor

TILE_SIZE = CONFIG['map']['tile_size']

class InGameController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.records_service = RecordsService()
        self._initialize_game()

    def _initialize_game(self):
        """Inicializa o reinicia el juego."""
        self.map = MapGrid(CONFIG['map']['width'], CONFIG['map']['height'])
        self.player = Player(x=1, y=1)
        self.enemies = []
        self.view = InGameView(self.screen, self.map, self.player, self.enemies)
        
        # Estado del juego
        self.is_paused = False
        self.game_time = 0.0
        self.last_update_time = time.time()
        self.current_round = 1
        self.enemies_remaining = 0
        self.total_enemies_killed = 0  # Contador total de enemigos eliminados
        self.is_dead = False
        
        # Estado del contador inicial
        self.countdown_active = True
        self.countdown_time = 3.0  # 3 segundos de cuenta regresiva
        self.countdown_start_time = time.time()
        
        # Solo crear el jugador y enemigos si no estamos en modo debug del mapa
        if not CONFIG['debug']['map_only']:
            self._spawn_enemies()

    def _calculate_enemy_count(self, level: int) -> int:
        """Calcula la cantidad de enemigos para un nivel específico en la ronda actual."""
        n = 2**self.current_round - 1
        return floor(n / level)

    def _spawn_enemies(self):
        """Genera los enemigos para la ronda actual."""
        self.enemies.clear()
        
        # Generar enemigos según la progresión geométrica
        # Nivel 1: Enemigos básicos
        for _ in range(self._calculate_enemy_count(1)):
            x, y = self.map.get_random_floor_position()
            self.enemies.append(BasicEnemy(x, y))
        
        # Nivel 2: Enemigos rápidos
        for _ in range(self._calculate_enemy_count(2)):
            x, y = self.map.get_random_floor_position()
            self.enemies.append(FastEnemy(x, y))
        
        # Nivel 3: Enemigos pesados
        for _ in range(self._calculate_enemy_count(3)):
            x, y = self.map.get_random_floor_position()
            self.enemies.append(HeavyEnemy(x, y))
        
        # Nivel 4: Enemigos a distancia
        for _ in range(self._calculate_enemy_count(4)):
            x, y = self.map.get_random_floor_position()
            self.enemies.append(RangedEnemy(x, y))
        
        # Nivel 5: Jefes
        for _ in range(self._calculate_enemy_count(5)):
            x, y = self.map.get_random_floor_position()
            self.enemies.append(BossEnemy(x, y))
            
        self.enemies_remaining = len(self.enemies)

    def _check_round_completion(self):
        """Verifica si se han eliminado todos los enemigos de la ronda actual."""
        alive_enemies = sum(1 for enemy in self.enemies if enemy.is_alive)
        self.enemies_remaining = alive_enemies
        
        # Actualizar contador de enemigos eliminados
        dead_enemies = sum(1 for enemy in self.enemies if not enemy.is_alive)
        self.total_enemies_killed = dead_enemies  # Contar solo los enemigos muertos actuales
        # BUG: El contador de enemigos eliminados no se actualiza correctamente puesto que no refleja el total de enemigos eliminados en la partida sino solo los eliminados en la ronda actual
        if alive_enemies == 0:
            self.current_round += 1
            self._spawn_enemies()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_paused = not self.is_paused
                if self.is_paused:
                    self.last_update_time = time.time()
                return
            elif event.key == pygame.K_r and self.is_dead:
                self._reset_game()
                return
                
        if not self.is_paused and not self.is_dead and not CONFIG['debug']['map_only']:
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self._handle_movement(event)
            if event.type == pygame.KEYDOWN:
                self._handle_attack(event.key)

    def _handle_movement(self, event: pygame.event.Event):
        """Maneja el movimiento del jugador."""
        is_key_down = event.type == pygame.KEYDOWN
        
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.player.move_up = is_key_down
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.player.move_down = is_key_down
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.player.move_left = is_key_down
        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.player.move_right = is_key_down

    def _handle_attack(self, key):
        """Maneja los ataques del jugador."""
        if key == pygame.K_k or key == pygame.K_x:  # Tecla K
            self.player.cast_uppercut((0,0))
        elif key == pygame.K_l or key == pygame.K_c:  # Tecla L
            self.player.cast_point_blank_explosion((0,0))

    def update(self, dt: float):
        """Actualiza el estado del juego."""
        if not self.is_paused and not self.is_dead:
            # Actualizar tiempo de juego
            current_time = time.time()
            
            # Actualizar contador inicial
            if self.countdown_active:
                elapsed = current_time - self.countdown_start_time
                if elapsed >= self.countdown_time:
                    self.countdown_active = False
                return  # No actualizar el juego mientras el contador está activo
            
            self.game_time += current_time - self.last_update_time
            self.last_update_time = current_time
            
            if not CONFIG['debug']['map_only']:
                # Verificar si el jugador está muerto
                if self.player.hp <= 0 and not self.is_dead:
                    self.is_dead = True
                    self.records_service.add_record(self.game_time, self.total_enemies_killed)
                    return
                
                # Actualizar jugador
                self.player.update(dt, self.map)
                
                # Actualizar ataques del jugador
                self.player._uppercut.update(dt)
                self.player._explosion.update(dt)
                
                # Actualizar enemigos y verificar colisiones con ataques
                for enemy in self.enemies:
                    if enemy.is_alive:
                        enemy.update(dt, self.player, self.map)
                        # Verificar si el enemigo es golpeado por algún ataque
                        enemy.check_attack_hit(self.player._uppercut)
                        enemy.check_attack_hit(self.player._explosion)
                
                # Verificar si se completó la ronda
                self._check_round_completion()

    def render(self):
        self.view.draw(
            self.is_paused,
            self.game_time,
            self.current_round,
            self.enemies_remaining,
            self.countdown_active,
            self.countdown_time - (time.time() - self.countdown_start_time) if self.countdown_active else 0,
            self.is_dead,
            self.total_enemies_killed
        )

    def _reset_game(self):
        """Reinicia el juego después de la muerte."""
        self._initialize_game()  # Reiniciar todo el juego desde cero
