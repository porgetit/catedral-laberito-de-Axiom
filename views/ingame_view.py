"""Vista pasiva de la escena de juego.
"""
import pygame
from services.config import CONFIG
from models.enemies import BasicEnemy, FastEnemy, HeavyEnemy, RangedEnemy, BossEnemy
import math

# Constantes de configuración
TILE_SIZE = CONFIG['map']['tile_size']
HITBOX_DEBUG = CONFIG['debug']['hitbox']

# Configuración del área de juego
GAME_AREA = CONFIG['game_area']
GAME_WIDTH = GAME_AREA['width']
GAME_HEIGHT = GAME_AREA['height']
MARGIN_LEFT = GAME_AREA['margins']['left']
MARGIN_TOP = GAME_AREA['margins']['top']

class InGameView:
    def __init__(self, screen: pygame.Surface, map_obj, player, enemies):
        self.screen = screen
        self.map = map_obj
        self.player = player
        self.enemies = enemies
        
        # Calcular el tamaño del mapa en píxeles
        self.map_width_px = self.map.width * TILE_SIZE
        self.map_height_px = self.map.height * TILE_SIZE
        
        # Calcular el offset para centrar el mapa en el área de juego
        self.offset_x = MARGIN_LEFT + (GAME_WIDTH - self.map_width_px) // 2
        self.offset_y = MARGIN_TOP + (GAME_HEIGHT - self.map_height_px) // 2
        
        # Configuración de fuentes
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.debug_font = pygame.font.Font(None, 20)

    def _draw_attack_effects(self):
        """Dibuja los efectos visuales de los ataques."""
        # Golpe Ascendente
        if self.player._uppercut.is_executing:
            dx, dy = self.player._uppercut.direction
            
            # Dibujar línea de dirección
            start_x = self.offset_x + int(self.player.x * TILE_SIZE) + TILE_SIZE//2
            start_y = self.offset_y + int(self.player.y * TILE_SIZE) + TILE_SIZE//2
            end_x = start_x + int(dx * self.player._uppercut.range_px)
            end_y = start_y + int(dy * self.player._uppercut.range_px)
            
            # Dibujar área de efecto
            pygame.draw.line(self.screen, (255, 200, 0), (start_x, start_y), (end_x, end_y), 2)
            pygame.draw.circle(self.screen, (255, 200, 0, 128), (end_x, end_y), 5)
            
        # Explosión a Quemarropa
        if self.player._explosion.is_executing:
            dx, dy = self.player._explosion.direction
            
            # Dibujar línea de dirección
            start_x = self.offset_x + int(self.player.x * TILE_SIZE) + TILE_SIZE//2
            start_y = self.offset_y + int(self.player.y * TILE_SIZE) + TILE_SIZE//2
            end_x = start_x + int(dx * self.player._explosion.range_px)
            end_y = start_y + int(dy * self.player._explosion.range_px)
            
            # Dibujar área de efecto
            pygame.draw.line(self.screen, (255, 0, 0), (start_x, start_y), (end_x, end_y), 2)
            pygame.draw.circle(self.screen, (255, 0, 0, 128), (end_x, end_y), 8)

    def draw(self, is_paused: bool, game_time: float):
        """Dibuja el mapa, el jugador, los enemigos y la UI."""
        # Limpiar pantalla con color de fondo
        self.screen.fill((0, 0, 0))  # Fondo negro
        
        # Dibujar área de juego
        game_rect = pygame.Rect(MARGIN_LEFT, MARGIN_TOP, GAME_WIDTH, GAME_HEIGHT)
        self.screen.fill((30, 30, 30), game_rect)  # Fondo gris oscuro
        
        # Dibujar mapa y entidades
        self._draw_game_entities()
        
        # Dibujar efectos de ataques
        self._draw_attack_effects()
        
        # Dibujar UI
        self._draw_ui(is_paused, game_time)
        
        # Dibujar mensaje de pausa si está pausado
        if is_paused:
            self._draw_pause_message()

    def _draw_game_entities(self):
        """Dibuja el mapa, jugador y enemigos."""
        # Dibujar mapa
        for y in range(self.map.height):
            for x in range(self.map.width):
                rect = pygame.Rect(
                    self.offset_x + x * TILE_SIZE,
                    self.offset_y + y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
                color = tuple(CONFIG['map']['colors']['floor']) if self.map.is_walkable(x, y) else tuple(CONFIG['map']['colors']['wall'])
                self.screen.fill(color, rect)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            if enemy.is_alive:
                px = self.offset_x + int(enemy.x * TILE_SIZE)
                py = self.offset_y + int(enemy.y * TILE_SIZE)
                
                # Seleccionar color según el tipo de enemigo
                if isinstance(enemy, BasicEnemy):
                    color = tuple(CONFIG['enemies']['basic']['color'])
                elif isinstance(enemy, FastEnemy):
                    color = tuple(CONFIG['enemies']['fast']['color'])
                elif isinstance(enemy, HeavyEnemy):
                    color = tuple(CONFIG['enemies']['heavy']['color'])
                elif isinstance(enemy, RangedEnemy):
                    color = tuple(CONFIG['enemies']['ranged']['color'])
                elif isinstance(enemy, BossEnemy):
                    color = tuple(CONFIG['enemies']['boss']['color'])
                else:
                    color = tuple(CONFIG['enemies']['basic']['color'])
                
                self.screen.fill(color, pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))
                
                if HITBOX_DEBUG:
                    pygame.draw.rect(
                        self.screen,
                        color,
                        enemy.hitbox.get_scaled_rect(TILE_SIZE).move(self.offset_x, self.offset_y),
                        1
                    )
        
        # Dibujar jugador
        px = self.offset_x + int(self.player.x * TILE_SIZE)
        py = self.offset_y + int(self.player.y * TILE_SIZE)
        self.screen.fill(tuple(CONFIG['player']['colors']['body']),
                         pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))

        # Dibuja el hitbox del jugador si está activado el modo debug
        if HITBOX_DEBUG:
            pygame.draw.rect(
                self.screen,
                tuple(CONFIG['player']['colors']['hitbox']),
                self.player.hitbox.get_scaled_rect(TILE_SIZE).move(self.offset_x, self.offset_y),
                1
            )
            # Hitbox de muros
            for y in range(self.map.height):
                for x in range(self.map.width):
                    wall_hitbox = self.map.get_wall_hitbox(x, y)
                    if wall_hitbox:
                        pygame.draw.rect(
                            self.screen,
                            tuple(CONFIG['map']['colors']['debug']['wall']),
                            wall_hitbox.get_scaled_rect(TILE_SIZE).move(self.offset_x, self.offset_y),
                            1
                        )

    def _draw_ui(self, is_paused: bool, game_time: float):
        """Dibuja la interfaz de usuario."""
        # Dibujar panel de estadísticas
        stats_x = 20
        stats_y = 20
        
        # Título
        title = self.title_font.render("Estadísticas del Jugador", True, (255, 255, 255))
        self.screen.blit(title, (stats_x, stats_y))
        
        # HP
        hp_text = self.font.render(f"HP: {self.player.hp}", True, (255, 0, 0))
        self.screen.blit(hp_text, (stats_x, stats_y + 40))
        
        # MP
        mp_text = self.font.render(f"MP: {self.player.mp}", True, (0, 0, 255))
        self.screen.blit(mp_text, (stats_x, stats_y + 70))
        
        # Tiempo de juego
        minutes = int(game_time // 60)
        seconds = int(game_time % 60)
        time_text = self.font.render(f"Tiempo: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        self.screen.blit(time_text, (stats_x, stats_y + 100))
        
        # Controles
        controls_y = MARGIN_TOP + GAME_HEIGHT + 20
        controls = [
            "Controles:",
            "WASD - Movimiento",
            "Click Izq - Golpe Ascendente",
            "Click Der - Explosión a Quemarropa",
            "ESC - Pausar/Reanudar"
        ]
        
        for i, text in enumerate(controls):
            control_text = self.font.render(text, True, (200, 200, 200))
            self.screen.blit(control_text, (stats_x, controls_y + i * 30))

    def _draw_pause_message(self):
        """Dibuja el mensaje de pausa."""
        # Crear una superficie semi-transparente
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (MARGIN_LEFT, MARGIN_TOP))
        
        # Mensaje de pausa
        pause_text = self.title_font.render("PAUSA", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(MARGIN_LEFT + GAME_WIDTH//2, MARGIN_TOP + GAME_HEIGHT//2))
        self.screen.blit(pause_text, text_rect)
        
        # Instrucción
        continue_text = self.font.render("Presiona ESC para continuar", True, (200, 200, 200))
        continue_rect = continue_text.get_rect(center=(MARGIN_LEFT + GAME_WIDTH//2, MARGIN_TOP + GAME_HEIGHT//2 + 40))
        self.screen.blit(continue_text, continue_rect)

    def _draw_debug_info(self, map_grid, player, enemies):
        """Dibuja información de debug."""
        # Información del mapa
        map_info = f"Mapa: {map_grid.width}x{map_grid.height}"
        text = self.debug_font.render(map_info, True, (200, 200, 200))
        self.screen.blit(text, (10, 10))
        
        # Información del jugador
        if player:
            player_info = f"Jugador: ({player.x:.1f}, {player.y:.1f})"
            text = self.debug_font.render(player_info, True, (200, 200, 200))
            self.screen.blit(text, (10, 30))
        
        # Información de enemigos
        if enemies:
            enemy_info = f"Enemigos vivos: {sum(1 for e in enemies if e.is_alive)}"
            text = self.debug_font.render(enemy_info, True, (200, 200, 200))
            self.screen.blit(text, (10, 50))
