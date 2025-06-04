"""Modelo del jugador con movimiento y ataques básicos.
"""
from models.entity import Entity
from models.hitbox import Hitbox
from models.attacks import basicAttack, heavyAttack
from services.config import CONFIG
from dataclasses import dataclass, field
from math import floor, ceil
import time
import pygame
from typing import Dict, Tuple

@dataclass
class Player(Entity):
    hp: int = CONFIG['player']['hp']
    mp: int = CONFIG['player']['mp']
    width: int = CONFIG['player']['width']
    height: int = CONFIG['player']['height']
    _basic_attack_cooldown: float = field(default=0.0, init=False, repr=False)
    _heavy_attack_cooldown: float = field(default=0.0, init=False, repr=False)
    _basic_attack: basicAttack = field(default_factory=basicAttack, init=False, repr=False)
    _heavy_attack: heavyAttack = field(default_factory=heavyAttack, init=False, repr=False)
    _last_regen_time: float = field(default_factory=time.time, init=False, repr=False)

    # Input flags
    move_up: bool = field(default=False, repr=False)
    move_down: bool = field(default=False, repr=False)
    move_left: bool = field(default=False, repr=False)
    move_right: bool = field(default=False, repr=False)

    def update(self, dt: float, map_obj):
        # Movimiento propuesto
        dx = (self.move_right - self.move_left) * CONFIG['player']['speed'] * dt
        dy = (self.move_down - self.move_up) * CONFIG['player']['speed'] * dt

        # Verificar colisiones por separado en X e Y
        new_x = self.x + dx
        new_y = self.y + dy

        # Intentar movimiento en X
        if dx != 0 and self._can_move_to(new_x, self.y, map_obj):
            self.x = new_x

        # Intentar movimiento en Y
        if dy != 0 and self._can_move_to(self.x, new_y, map_obj):
            self.y = new_y

        # Enfriamiento de los ataques
        if self._basic_attack_cooldown > 0:
            self._basic_attack_cooldown -= dt
        if self._heavy_attack_cooldown > 0:
            self._heavy_attack_cooldown -= dt

        # Regeneración de HP y MP
        current_time = time.time()
        if current_time - self._last_regen_time >= CONFIG['player']['time_to_regen']:
            # Regenerar HP
            if self.hp < CONFIG['player']['hp']:
                # Convertir el porcentaje a decimal (0.1% = 0.001)
                hp_regen_percent = CONFIG['player']['hp_regen'] / 100
                hp_regen = CONFIG['player']['hp'] * hp_regen_percent
                self.hp = min(self.hp + hp_regen, CONFIG['player']['hp'])
            
            # Regenerar MP
            if self.mp < CONFIG['player']['mp']:
                # Convertir el porcentaje a decimal (0.1% = 0.001)
                mp_regen_percent = CONFIG['player']['mp_regen'] / 100
                mp_regen = CONFIG['player']['mp'] * mp_regen_percent
                self.mp = min(self.mp + mp_regen, CONFIG['player']['mp'])
            
            self._last_regen_time = current_time
            
    def _can_move_to(self, new_x: float, new_y: float, map_obj) -> bool:
        """Verifica si la entidad puede moverse a la nueva posición."""
        player_hitbox = Hitbox(new_x, new_y, self.width, self.height)
        min_x = floor(new_x)
        max_x = ceil(new_x + self.width - 1e-6)
        min_y = floor(new_y)
        max_y = ceil(new_y + self.height - 1e-6)
        try:
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    wall_hitbox = map_obj.get_wall_hitbox(x, y)
                    if wall_hitbox and player_hitbox.collides_with(wall_hitbox):
                        return False
        except IndexError:
            return False
        return True
        
    def cast_basic_attack(self, direction: tuple[float, float] = None):
        """Ejecuta el ataque básico y actualiza la animación."""
        if self._basic_attack_cooldown <= 0:
            # Calcular el centro del jugador
            center_x = self.x + (self.width / 2)
            center_y = self.y + (self.height / 2)
            self._basic_attack.execute(center_x, center_y, direction)
            self._basic_attack_cooldown = self._basic_attack.cooldown
            
            # Actualizar estado de animación
            self.state = "attack1"
            self.is_attacking = True
            self.attack_frame = 0
            self.attack_complete = False
            
    def cast_heavy_attack(self, direction: tuple[float, float] = None):
        """Ejecuta el ataque pesado y actualiza la animación."""
        if self._heavy_attack_cooldown <= 0 and self.mp >= self._heavy_attack.mp_cost:
            # Calcular el centro del jugador
            center_x = self.x + (self.width / 2)
            center_y = self.y + (self.height / 2)
            self.mp -= self._heavy_attack.mp_cost
            self._heavy_attack.execute(center_x, center_y, direction)
            self._heavy_attack_cooldown = self._heavy_attack.cooldown
            
            # Actualizar estado de animación
            self.state = "attack2"
            self.is_attacking = True
            self.attack_frame = 0
            self.attack_complete = False
            
class AnimatedPlayer(Player):
    """
    Clase que representa al personaje jugable con animaciones.
    
    Esta clase maneja:
    - Animaciones del personaje (idle, run, attack1, attack2)
    - Movimiento del personaje
    - Estados del personaje
    - Colisiones y límites de la pantalla
    
    Attributes:
        state (str): Estado actual del personaje ('idle', 'run', 'attack1', 'attack2')
        direction (str): Dirección actual del personaje ('up', 'down', 'left', 'right')
        speed (int): Velocidad de movimiento del personaje
    """
    
    # Constantes de la clase
    SPRITE_SIZE = (52, 62)
    ANIMATION_DELAY = 100
    MOVEMENT_SPEED = 5
    
    def __init__(self, x: int, y: int):
        """
        Inicializa el personaje jugable.
        
        Args:
            x (int): Posición inicial X del personaje
            y (int): Posición inicial Y del personaje
        """
        super().__init__(x=x, y=y)
        
        # Cargar y escalar sprites
        self._load_sprites()
        
        # Estados y animaciones
        self.state = "idle"
        self.direction = "down"
        self.frame = 0
        self.animation_timer = 0
        self.animation_delay = self.ANIMATION_DELAY
        
        # Imagen inicial
        self.image = self._get_initial_image()
        
        # Estados de animación con rectángulos corregidos
        self.states = self._initialize_animation_states()
        
        # Variables para control de ataques
        self.attack_frame = 0
        self.is_attacking = False
        self.attack_complete = False

    def _load_sprites(self) -> None:
        """Carga y escala todos los sprites necesarios para las animaciones."""
        # Cargar sprites
        self.sheet_idle_down = pygame.image.load("assets/PJ/Sprites/IDLE/idle_down.png")
        self.sheet_idle_up = pygame.image.load("assets/PJ/Sprites/IDLE/idle_up.png")
        self.sheet_idle_left = pygame.image.load("assets/PJ/Sprites/IDLE/idle_left.png")
        self.sheet_idle_right = pygame.image.load("assets/PJ/Sprites/IDLE/idle_right.png")
        
        self.sheet_run_down = pygame.image.load("assets/PJ/Sprites/RUN/run_down.png")
        self.sheet_run_up = pygame.image.load("assets/PJ/Sprites/RUN/run_up.png")
        self.sheet_run_left = pygame.image.load("assets/PJ/Sprites/RUN/run_left.png")
        self.sheet_run_right = pygame.image.load("assets/PJ/Sprites/RUN/run_right.png")
        
        self.sheet_attack1_down = pygame.image.load("assets/PJ/Sprites/ATTACK 1/attack1_down.png")
        self.sheet_attack1_up = pygame.image.load("assets/PJ/Sprites/ATTACK 1/attack1_up.png")
        self.sheet_attack1_left = pygame.image.load("assets/PJ/Sprites/ATTACK 1/attack1_left.png")
        self.sheet_attack1_right = pygame.image.load("assets/PJ/Sprites/ATTACK 1/attack1_right.png")
        
        self.sheet_attack2_down = pygame.image.load("assets/PJ/Sprites/ATTACK 2/attack2_down.png")
        self.sheet_attack2_up = pygame.image.load("assets/PJ/Sprites/ATTACK 2/attack2_up.png")
        self.sheet_attack2_left = pygame.image.load("assets/PJ/Sprites/ATTACK 2/attack2_left.png")
        self.sheet_attack2_right = pygame.image.load("assets/PJ/Sprites/ATTACK 2/attack2_right.png")
        
        # Escalar sprites
        for sheet in [self.sheet_idle_down, self.sheet_idle_up, self.sheet_idle_left, self.sheet_idle_right,
                     self.sheet_run_down, self.sheet_run_up, self.sheet_run_left, self.sheet_run_right,
                     self.sheet_attack1_down, self.sheet_attack1_up, self.sheet_attack1_left, self.sheet_attack1_right,
                     self.sheet_attack2_down, self.sheet_attack2_up, self.sheet_attack2_left, self.sheet_attack2_right]:
            sheet = pygame.transform.scale(sheet, self.SPRITE_SIZE)

    def _get_initial_image(self) -> pygame.Surface:
        """Retorna la imagen inicial del personaje."""
        image = self.sheet_idle_down.subsurface(pygame.Rect(35, 22, 20, 30))
        return pygame.transform.scale(image, self.SPRITE_SIZE)

    def _initialize_animation_states(self) -> Dict:
        """Inicializa y retorna los estados de animación con sus respectivos frames."""
        return {
            "idle": {
                "down": [(35, 22, 20, 35), (133, 22, 20, 35), (229, 22, 20, 35), (325, 22, 20, 35)],
                "up": [(35, 22, 20, 35), (133, 22, 20, 35), (229, 22, 20, 35), (325, 22, 20, 35)],
                "left": [(35, 22, 20, 35), (133, 22, 20, 35), (229, 22, 20, 35), (325, 22, 20, 35)],
                "right": [(35, 22, 20, 35), (133, 22, 20, 35), (229, 22, 20, 35), (325, 22, 20, 35)]
            },
            "run": {
                "down": [(133, 27, 20, 35), (229, 27, 20, 35), (325, 27, 20, 35), (421, 27, 20, 35)],
                "up": [(133, 27, 20, 35), (229, 27, 20, 35), (325, 27, 20, 35), (421, 27, 20, 35)],
                "left": [(133, 27, 20, 35), (229, 27, 20, 35), (325, 27, 20, 35), (421, 27, 20, 35)],
                "right": [(133, 27, 20, 35), (229, 27, 20, 35), (325, 27, 20, 35), (421, 27, 20, 35)]
            },
            "attack1": {
                "down": [(113, 27, 45, 35), (229, 27, 45, 35), (325, 27, 45, 35), (421, 27, 45, 35)],
                "up": [(113, 14, 45, 35), (207, 14, 45, 35), (304, 27, 45, 35), (414, 27, 45, 35)],
                "left": [(102, 27, 45, 35), (202, 27, 45, 35), (314, 27, 45, 35), (414, 27, 45, 35)],
                "right": [(137, 27, 45, 35), (229, 27, 45, 35), (325, 27, 45, 35), (421, 27, 45, 35)]
            },
            "attack2": {
                "down": [(113, 27, 45, 35), (207, 27, 45, 35), (304, 27, 45, 35), (402, 27, 45, 35)],
                "up": [(116, 16, 45, 35), (230, 16, 45, 35), (326, 24, 45, 35), (422, 24, 45, 35)],
                "left": [(100, 24, 45, 35), (196, 27, 45, 35), (314, 27, 45, 35), (408, 27, 45, 35)],
                "right": [(137, 27, 45, 35), (224, 27, 45, 35), (321, 27, 45, 35), (418, 27, 45, 35)]
            }
        }

    def get_current_sheet(self) -> pygame.Surface:
        """
        Retorna la hoja de sprites actual según el estado y dirección del personaje.
        
        Returns:
            pygame.Surface: La hoja de sprites correspondiente al estado actual
        """
        return getattr(self, f"sheet_{self.state}_{self.direction}")

    def update(self, dt: float, map_obj):
        """Actualiza el estado del personaje, incluyendo animaciones y movimiento."""
        # Actualizar animación
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.animation_timer = current_time
            self._update_animation()
        
        # Actualizar movimiento y lógica del juego
        super().update(dt, map_obj)
        
        # Actualizar estado de animación basado en el movimiento
        if not self.is_attacking:
            if self.move_up or self.move_down or self.move_left or self.move_right:
                self.state = "run"
            else:
                self.state = "idle"
            
            # Actualizar dirección basada en el movimiento
            if self.move_up:
                self.direction = "up"
            elif self.move_down:
                self.direction = "down"
            elif self.move_left:
                self.direction = "left"
            elif self.move_right:
                self.direction = "right"

    def _update_animation(self) -> None:
        """Actualiza el frame de animación actual."""
        # Manejo especial para ataques
        if self.state in ["attack1", "attack2"]:
            if self.is_attacking:
                self.attack_frame += 1
                if self.attack_frame >= len(self.states[self.state][self.direction]):
                    self.is_attacking = False
                    self.attack_frame = 0
                    self.state = "idle"
                    self.attack_complete = True
            else:
                self.frame = 0
        else:
            self.frame = (self.frame + 1) % len(self.states[self.state][self.direction])
        
        # Obtener y actualizar el frame actual
        current_frame = self._get_current_frame()
        current_sheet = self.get_current_sheet()
        self.image = current_sheet.subsurface(pygame.Rect(current_frame))
        self.image = pygame.transform.scale(self.image, self.SPRITE_SIZE)

    def _get_current_frame(self) -> Tuple[int, int, int, int]:
        """Retorna las coordenadas del frame actual de la animación."""
        if self.state in ["attack1", "attack2"] and self.is_attacking:
            return self.states[self.state][self.direction][self.attack_frame]
        return self.states[self.state][self.direction][self.frame]

    def cast_basic_attack(self, direction: tuple[float, float] = None):
        """Ejecuta el ataque básico y actualiza la animación."""
        if self._basic_attack_cooldown <= 0:
            # Calcular el centro del jugador
            center_x = self.x + (self.width / 2)
            center_y = self.y + (self.height / 2)
            self._basic_attack.execute(center_x, center_y, direction)
            self._basic_attack_cooldown = self._basic_attack.cooldown
            
            # Actualizar estado de animación
            self.state = "attack1"
            self.is_attacking = True
            self.attack_frame = 0
            self.attack_complete = False
            
    def cast_heavy_attack(self, direction: tuple[float, float] = None):
        """Ejecuta el ataque pesado y actualiza la animación."""
        if self._heavy_attack_cooldown <= 0 and self.mp >= self._heavy_attack.mp_cost:
            # Calcular el centro del jugador
            center_x = self.x + (self.width / 2)
            center_y = self.y + (self.height / 2)
            self.mp -= self._heavy_attack.mp_cost
            self._heavy_attack.execute(center_x, center_y, direction)
            self._heavy_attack_cooldown = self._heavy_attack.cooldown
            
            # Actualizar estado de animación
            self.state = "attack2"
            self.is_attacking = True
            self.attack_frame = 0
            self.attack_complete = False
            
