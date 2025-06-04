"""Controlador de la escena de juego en curso.

Maneja entrada WASD y actualiza los modelos Player, Map y Enemies.

"""
import pygame
import time
from math import floor, log
from models.player import AnimatedPlayer
from models.map_grid import MapGrid
from models.pause_menu import PauseMenuModel
from models.enemies import Enemy
from views.ingame_view import InGameView
from views.pause_menu_view import PauseMenuView
from services.config import CONFIG
from services.records import RecordsService
from services.audio_manager import AudioManager

TILE_SIZE = CONFIG['map']['tile_size']
VICTORY_ROUND = 4

class InGameController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.records_service = RecordsService()
        self.audio_manager = AudioManager()
        self.pause_menu_model = PauseMenuModel()
        self.pause_menu_view = PauseMenuView(screen, self.pause_menu_model)
        self._initialize_game()

    def _initialize_game(self):
        """Inicializa el juego y sus componentes principales."""
        self.map = MapGrid(CONFIG['map']['width'], CONFIG['map']['height'])
        self.player = AnimatedPlayer(x=1, y=1)
        self.enemies = []
        self.view = InGameView(self.screen, self.map, self.player, self.enemies)
        
        # Estado del juego
        self.is_paused = False
        self.game_time = 0.0
        self.last_update_time = time.time()
        self.current_round = 1
        self.enemies_remaining = 0
        self.is_dead = False
        self.has_won = False
        self.points = 0
        
        # Estado del contador inicial
        self.countdown_active = True
        self.countdown_time = 3.0  # 3 segundos de cuenta regresiva
        self.countdown_start_time = time.time()
        
        # Estado de generación de enemigos
        self.enemy_generation_queue = []
        self.is_generating_enemies = False
        
        self._spawn_enemies()
            

    def _calculate_enemy_count(self, level: int) -> int:
        """Calcula la cantidad de enemigos para un nivel específico en la ronda actual."""
        n = max(1, int(2 * log(self.current_round + 1))) # Progresión logarítmica: 1-2-3-4-4-5
        return floor(n / level)

    def _spawn_enemies(self):
        """Genera los enemigos para la ronda actual."""
        self.enemies.clear()
        
        # Define los niveles de enemigos disponibles
        enemy_levels = range(1, 6)  # Niveles del 1 al 5
        
        # Genera enemigos de cada nivel
        for level in enemy_levels:
            count = self._calculate_enemy_count(level)
            self._spawn_enemies_of_level(level, count)
                
        self.enemies_remaining = len(self.enemies)
        
        # Configurar callback de muerte para cada enemigo
        for enemy in self.enemies:
            enemy._death_complete_callback = self._on_enemy_death_complete

    def _spawn_enemies_of_level(self, level: int, count: int):
        """Genera una cantidad específica de enemigos de un nivel dado."""
        for _ in range(count):
            x, y = self.map.get_random_floor_position()
            enemy = Enemy(x, y, level)  # Asumiendo que existe una clase base Enemy
            self.enemies.append(enemy)

    def _on_enemy_death_complete(self, enemy):
        """Callback que se ejecuta cuando un enemigo completa su animación de muerte."""
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            self.enemies_remaining = len([e for e in self.enemies if e.is_alive])
            
            # Verificar si se completó la ronda
            if self.enemies_remaining == 0:
                self._start_next_round()

    def _start_next_round(self):
        """Inicia la siguiente ronda de enemigos."""
        self.current_round += 1
        if self.current_round <= VICTORY_ROUND:
            self._spawn_enemies()
        else:
            self.has_won = True
            self.records_service.add_record(self.points)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_paused = not self.is_paused
                if self.is_paused:
                    self.last_update_time = time.time()
                    self.audio_manager.pause_all()
                else:
                    self.audio_manager.unpause_all()
                return
            elif event.key == pygame.K_r and (self.is_dead or self.has_won):
                self._reset_game()
                return

        # Manejar clicks en el menú de pausa
        if self.is_paused and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo
                for i, rect in enumerate(self.pause_menu_view.get_button_rects()):
                    if rect.collidepoint(event.pos):
                        option = self.pause_menu_model.get_button_labels()[i]
                        if option == "Continuar":
                            self.is_paused = False
                            self.last_update_time = time.time()
                            self.audio_manager.unpause_all()
                        elif option == "Salir al Menú":
                            return "menu"  # Señal para volver al menú principal
                return
        
        # Manejar clicks en pantallas de muerte/victoria
        if (self.is_dead or self.has_won) and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo
                if hasattr(self.view, 'restart_button_rect') and self.view.restart_button_rect.collidepoint(event.pos):
                    self._initialize_game()
                elif hasattr(self.view, 'menu_button_rect') and self.view.menu_button_rect.collidepoint(event.pos):
                    return "menu"
            return

        if not self.is_paused and not self.is_dead and not self.has_won:
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
        if key == pygame.K_x or key == pygame.K_k:  # Ataque básico
            self.player.cast_basic_attack()
            self.audio_manager.play_attack_sound()
        elif key == pygame.K_c or key == pygame.K_l:  # Ataque pesado
            self.player.cast_heavy_attack()
            self.audio_manager.play_attack_sound()

    def update(self, dt: float):
        """Actualiza el estado del juego."""
        if not self.is_paused and not self.is_dead and not self.has_won:
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
            
            # Actualizar puntos por tiempo (1 punto por segundo)
            self.points = int(self.game_time)
            
            # Verificar si el jugador está muerto
            if self.player.hp <= 0 and not self.is_dead:
                self.is_dead = True
                return
            
            # Actualizar jugador
            self.player.update(dt, self.map)
            
            # Actualizar ataques del jugador
            self.player._basic_attack.update(dt)
            self.player._heavy_attack.update(dt)
            
            # Actualizar enemigos y verificar colisiones con ataques
            for enemy in self.enemies:
                if not enemy.is_alive:
                    continue                    
                enemy.update(dt, self.player, self.map)
                enemy.check_attack_hit(self.player._basic_attack)
                enemy.check_attack_hit(self.player._heavy_attack)
                
    def render(self):
        # Primero renderizar el juego
        self.view.draw(
            False,  # No mostrar mensaje de pausa, ahora usamos el menú
            self.points,
            self.current_round,
            self.enemies_remaining,
            self.countdown_active,
            self.countdown_time - (time.time() - self.countdown_start_time) if self.countdown_active else 0,
            self.is_dead,
            self.has_won
        )
        
        # Si está pausado, renderizar el menú de pausa encima
        if self.is_paused:
            self.pause_menu_view.draw()

    def _reset_game(self):
        """Reinicia el juego después de la muerte o victoria."""
        self._initialize_game()  # Reiniciar todo el juego desde cero
