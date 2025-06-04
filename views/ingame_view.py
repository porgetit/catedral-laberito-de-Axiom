"""Vista pasiva de la escena de juego.
"""
import pygame
from services.config import CONFIG

# Constantes de configuración
TILE_SIZE = CONFIG['map']['tile_size']
HITBOX_DEBUG = CONFIG['debug']['hitbox']

# Configuración del área de juego
GAME_AREA = CONFIG['game_area']
GAME_WIDTH = GAME_AREA['width']
GAME_HEIGHT = GAME_AREA['height']
MARGIN_LEFT = GAME_AREA['margins']['left']
MARGIN_TOP = GAME_AREA['margins']['top']

# Configuración del panel de información
INFO_PANEL = GAME_AREA['info_panel']
PANEL_WIDTH = INFO_PANEL['width']
PANEL_PADDING = INFO_PANEL['padding']
PANEL_BG = INFO_PANEL['background']
TEXT_COLOR = INFO_PANEL['text_color']
TITLE_COLOR = INFO_PANEL['title_color']

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
        self.countdown_font = pygame.font.Font(None, 72)
        self.death_font = pygame.font.Font(None, 48)
        self.victory_font = pygame.font.Font(None, 48)

    def _draw_attack_effects(self):
        """Dibuja los efectos visuales de los ataques."""

        # Calcular el centro del jugador
        center_x = self.offset_x + int(self.player.x * TILE_SIZE) + TILE_SIZE//2
        center_y = self.offset_y + int(self.player.y * TILE_SIZE) + TILE_SIZE//2
        # Golpe Ascendente
        if self.player._basic_attack.is_executing:
            # Dibujar área de efecto circular
            radius = int(self.player._basic_attack.range * TILE_SIZE)
            pygame.draw.circle(self.screen, (255, 200, 0, 128), (center_x, center_y), radius, 2) # NOTE: El color circulo no se ha establecido en el config.yaml porque este objeto solo se usa para desarrollo, no se renderiza en el juego final pues se reemplaza por el efecto visual del ataque
            
        # Explosión a Quemarropa
        if self.player._heavy_attack.is_executing:            
            # Dibujar área de efecto circular
            radius = int(self.player._heavy_attack.range * TILE_SIZE)
            pygame.draw.circle(self.screen, (255, 0, 0, 128), (center_x, center_y), radius, 2) # NOTE: El color circulo no se ha establecido en el config.yaml porque este objeto solo se usa para desarrollo, no se renderiza en el juego final pues se reemplaza por el efecto visual del ataque
            
            
    def draw(self, is_paused: bool, game_time: float, current_round: int, enemies_remaining: int, countdown_active: bool, countdown_time: float, is_dead: bool, has_won: bool):
        """Dibuja el mapa, el jugador, los enemigos y la UI."""
        # Limpiar pantalla con color de fondo
        self.screen.fill((0, 0, 0))  # Fondo negro
        
        # Dibujar panel de información
        self._draw_info_panel(game_time, current_round, enemies_remaining)
        
        # Dibujar área de juego
        game_rect = pygame.Rect(MARGIN_LEFT, MARGIN_TOP, GAME_WIDTH, GAME_HEIGHT)
        self.screen.fill((30, 30, 30), game_rect)  # TODO: Direccionar el color del fondo a config.yaml
        
        # Dibujar mapa y entidades
        self._draw_game_entities()
        
        # Dibujar efectos de ataques
        self._draw_attack_effects()
        
        # Dibujar contador inicial si está activo
        if countdown_active:
            self._draw_countdown(countdown_time)
        
        # Dibujar pantalla de muerte si el jugador está muerto
        if is_dead:
            self._draw_death_screen(game_time)
        
        # Dibujar pantalla de victoria si el jugador ha ganado
        if has_won:
            self._draw_victory_screen(game_time)
        
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
                
                # Obtener el color del enemigo según su nivel
                color = tuple(CONFIG['enemies'][f'level_{enemy.level}']['color'])
                
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

    def _draw_info_panel(self, game_time: float, current_round: int, enemies_remaining: int):
        """Dibuja el panel de información en el lado izquierdo."""
        # Dibujar fondo del panel
        panel_rect = pygame.Rect(0, 0, PANEL_WIDTH, self.screen.get_height())
        self.screen.fill(PANEL_BG, panel_rect)
        
        # Título del panel
        title = self.title_font.render("Información del Juego", True, TITLE_COLOR)
        self.screen.blit(title, (PANEL_PADDING, PANEL_PADDING))
        
        # Información del juego
        y_offset = PANEL_PADDING * 3
        line_height = 30
        
        # Puntos
        points = int(game_time)  # Convertir tiempo a puntos (1 punto por segundo)
        points_text = f"Puntos: {points}"
        points_surface = self.font.render(points_text, True, TEXT_COLOR)
        self.screen.blit(points_surface, (PANEL_PADDING, y_offset))
        y_offset += line_height
        
        # Ronda actual
        round_text = f"Ronda: {current_round}/10"
        round_surface = self.font.render(round_text, True, TEXT_COLOR)
        self.screen.blit(round_surface, (PANEL_PADDING, y_offset))
        y_offset += line_height
        
        # Enemigos restantes
        enemies_text = f"Enemigos: {enemies_remaining}"
        enemies_surface = self.font.render(enemies_text, True, TEXT_COLOR)
        self.screen.blit(enemies_surface, (PANEL_PADDING, y_offset))
        y_offset += line_height
        
        # Vida del jugador
        hp_text = f"HP: {self.player.hp}"
        hp_surface = self.font.render(hp_text, True, TEXT_COLOR)
        self.screen.blit(hp_surface, (PANEL_PADDING, y_offset))
        y_offset += line_height
        
        # MP del jugador
        mp_text = f"MP: {self.player.mp}"
        mp_surface = self.font.render(mp_text, True, TEXT_COLOR)
        self.screen.blit(mp_surface, (PANEL_PADDING, y_offset))
        y_offset += line_height
        
        # Información de ataques
        y_offset += line_height
        attacks_title = self.font.render("Ataques:", True, TITLE_COLOR)
        self.screen.blit(attacks_title, (PANEL_PADDING, y_offset))
        y_offset += line_height
        
        # Golpe liviano
        basic_attack_text = f"{CONFIG['attacks']['melee']['basic']['name']} (K)"
        basic_attack_surface = self.font.render(basic_attack_text, True, TEXT_COLOR)
        self.screen.blit(basic_attack_surface, (PANEL_PADDING, y_offset))
        y_offset += line_height
        
        # Golpe pesado
        heavy_attack_text = f"{CONFIG['attacks']['melee']['heavy']['name']} (L)"
        heavy_attack_surface = self.font.render(heavy_attack_text, True, TEXT_COLOR)
        self.screen.blit(heavy_attack_surface, (PANEL_PADDING, y_offset))

    def _draw_countdown(self, countdown_time: float):
        """Dibuja el contador inicial en el centro de la pantalla."""
        # Crear una superficie semi-transparente
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (MARGIN_LEFT, MARGIN_TOP))
        
        # Dibujar el número del contador
        count = str(int(countdown_time) + 1)  # +1 para mostrar el número actual
        count_surface = self.countdown_font.render(count, True, (255, 255, 255))
        count_rect = count_surface.get_rect(center=(MARGIN_LEFT + GAME_WIDTH//2, MARGIN_TOP + GAME_HEIGHT//2))
        self.screen.blit(count_surface, count_rect)

    def _draw_death_screen(self, game_time: float):
        """Dibuja la pantalla de muerte."""
        # Crear una superficie semi-transparente
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.fill((0, 0, 0)) # TODO: Direccionar el color del fondo a config.yaml
        overlay.set_alpha(192)  # Más oscuro que la pausa
        self.screen.blit(overlay, (MARGIN_LEFT, MARGIN_TOP))
        
        # Título
        title = self.death_font.render("¡HAS MUERTO!", True, (255, 0, 0))
        title_rect = title.get_rect(center=(MARGIN_LEFT + GAME_WIDTH//2, MARGIN_TOP + GAME_HEIGHT//2 - 60))
        self.screen.blit(title, title_rect)
        
        # Estadísticas
        stats_y = MARGIN_TOP + GAME_HEIGHT//2
        line_height = 40
        
        # Puntos finales
        points = int(game_time)
        points_text = f"Puntos finales: {points}"
        points_surface = self.title_font.render(points_text, True, (255, 255, 255))
        points_rect = points_surface.get_rect(center=(MARGIN_LEFT + GAME_WIDTH//2, stats_y))
        self.screen.blit(points_surface, points_rect)
        
        # Mensaje de reinicio
        restart_text = "Presiona R para reiniciar"
        restart_surface = self.font.render(restart_text, True, (200, 200, 200))
        restart_rect = restart_surface.get_rect(center=(MARGIN_LEFT + GAME_WIDTH//2, stats_y + line_height))
        self.screen.blit(restart_surface, restart_rect)

    def _draw_victory_screen(self, game_time: float):
        """Dibuja la pantalla de victoria."""
        # Crear una superficie semi-transparente
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(192)
        self.screen.blit(overlay, (MARGIN_LEFT, MARGIN_TOP))
        
        # Título
        title = self.victory_font.render("¡VICTORIA!", True, (0, 255, 0))
        title_rect = title.get_rect(center=(MARGIN_LEFT + GAME_WIDTH//2, MARGIN_TOP + GAME_HEIGHT//2 - 60))
        self.screen.blit(title, title_rect)
        
        # Estadísticas
        stats_y = MARGIN_TOP + GAME_HEIGHT//2
        line_height = 40
        
        # Puntos finales
        points = int(game_time)
        points_text = f"Puntos finales: {points}"
        points_surface = self.title_font.render(points_text, True, (255, 255, 255))
        points_rect = points_surface.get_rect(center=(MARGIN_LEFT + GAME_WIDTH//2, stats_y))
        self.screen.blit(points_surface, points_rect)
        
        # Mensaje de reinicio
        restart_text = "Presiona R para reiniciar"
        restart_surface = self.font.render(restart_text, True, (200, 200, 200))
        restart_rect = restart_surface.get_rect(center=(MARGIN_LEFT + GAME_WIDTH//2, stats_y + line_height))
        self.screen.blit(restart_surface, restart_rect)

    def _draw_pause_message(self):
        """Dibuja el mensaje de pausa."""
        # Crear una superficie semi-transparente
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (MARGIN_LEFT, MARGIN_TOP))
        
        # Mensaje de pausa
        pause_text = "PAUSA"
        pause_surface = self.title_font.render(pause_text, True, (255, 255, 255))
        pause_rect = pause_surface.get_rect(center=(MARGIN_LEFT + GAME_WIDTH//2, MARGIN_TOP + GAME_HEIGHT//2))
        self.screen.blit(pause_surface, pause_rect)

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
