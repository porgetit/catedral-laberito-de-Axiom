"""Sistema de enemigos del juego.

Contiene la clase base Enemy que maneja todos los tipos de enemigos según su nivel.
"""
from dataclasses import dataclass, field
from models.entity import Entity
from services.config import CONFIG
from math import atan2, cos, sin, floor, ceil, sqrt
from models.hitbox import Hitbox
import time
import pygame

@dataclass
class Enemy(Entity):
    """Clase base para todos los enemigos.
    """
    speed: float = 5.0
    damage: float = 10.0
    attack_range: float = 1.0
    attack_cooldown: float = 1.0
    level: int = 1
    _current_cooldown: float = 0.0
    _knockback_active: bool = field(default=False, init=False, repr=False)
    _knockback_start_time: float = field(default=0.0, init=False, repr=False)
    _knockback_direction: tuple[float, float] = field(default=(0.0, 0.0), init=False, repr=False)
    _knockback_force: float = field(default=0.0, init=False, repr=False)
    _knockback_velocity: tuple[float, float] = field(default=(0.0, 0.0), init=False, repr=False)
    _is_loading: bool = field(default=True, init=False, repr=False)
    
    # Variables para animación
    state: str = "idle"
    direction: str = "S"
    frame: int = 0
    animation_timer: float = 0.0
    animation_delay: float = 300.0
    attack_frame: int = 0
    is_attacking: bool = False
    is_dying: bool = False
    death_frame: int = 0
    is_dead: bool = False
    image: pygame.Surface = None
    SPRITE_SIZE = (32, 32)
    ANIMATION_DELAY = 300
    ATTACK_ANIMATION_DELAY = 100
    DEATH_ANIMATION_DELAY = 50  # Reducido para una animación más rápida
    ATTACK_RANGE = 3
    SCALE_FACTOR = 1.5
    render_order = 1
    _death_complete_callback = None  # Callback para notificar cuando la muerte está completa

    def __init__(self, x: float, y: float, level: int):
        """Inicializa un enemigo con estadísticas basadas en su nivel."""
        enemy_types = {
            1: 'level_1',
            2: 'level_2',
            3: 'level_3',
            4: 'level_4',
            5: 'level_5'
        }
        
        enemy_type = enemy_types[level]
        super().__init__(x=x, y=y)
        
        # Configurar estadísticas según el nivel
        self.speed = CONFIG['enemies'][enemy_type]['speed']
        self.damage = CONFIG['enemies'][enemy_type]['damage']
        self.level = level
        self.attack_range = self.ATTACK_RANGE
        
        # Definir colores por nivel
        self.level_colors = {
            1: (255, 0, 0, 200),    # Rojo semi-oscuro
            2: (0, 255, 0, 200),    # Verde semi-oscuro
            3: (0, 0, 255, 200),    # Azul semi-oscuro
            4: (255, 255, 0, 200),  # Amarillo semi-oscuro
            5: (255, 0, 255, 200)   # Magenta semi-oscuro
        }
        
        # Inicializar animaciones
        self._load_sprites()
        self.image = self._get_initial_image()
        self.states = self._initialize_animation_states()
        self._is_loading = False

    def _load_sprites(self) -> None:
        """Carga y escala todos los sprites necesarios para las animaciones."""
        try:
            # Cargar sprites de idle
            self.sheet_idle_n = pygame.image.load("assets/Enemies/IDLE/Enemy-Melee-Idle-N.png").convert_alpha()
            self.sheet_idle_s = pygame.image.load("assets/Enemies/IDLE/Enemy-Melee-Idle-S.png").convert_alpha()
            self.sheet_idle_e = pygame.image.load("assets/Enemies/IDLE/Enemy-Melee-Idle-E.png").convert_alpha()
            self.sheet_idle_w = pygame.image.load("assets/Enemies/IDLE/Enemy-Melee-Idle-W.png").convert_alpha()
            self.sheet_idle_nw = pygame.image.load("assets/Enemies/IDLE/Enemy-Melee-Idle-NE.png").convert_alpha()
            self.sheet_idle_ne = pygame.image.load("assets/Enemies/IDLE/Enemy-Melee-Idle-NW.png").convert_alpha()
            self.sheet_idle_se = pygame.image.load("assets/Enemies/IDLE/Enemy-Melee-Idle-SE.png").convert_alpha()
            self.sheet_idle_sw = pygame.image.load("assets/Enemies/IDLE/Enemy-Melee-Idle-SW.png").convert_alpha()
            
            # Cargar sprites de ataque
            self.sheet_attack_n = pygame.image.load("assets/Enemies/Attack/Enemy-Melee-Attack-N.png").convert_alpha()
            self.sheet_attack_s = pygame.image.load("assets/Enemies/Attack/Enemy-Melee-Attack-S.png").convert_alpha()
            self.sheet_attack_e = pygame.image.load("assets/Enemies/Attack/Enemy-Melee-Attack-E.png").convert_alpha()
            self.sheet_attack_w = pygame.image.load("assets/Enemies/Attack/Enemy-Melee-Attack-W.png").convert_alpha()
            self.sheet_attack_ne = pygame.image.load("assets/Enemies/Attack/Enemy-Melee-Attack-NE.png").convert_alpha()
            self.sheet_attack_nw = pygame.image.load("assets/Enemies/Attack/Enemy-Melee-Attack-NW.png").convert_alpha()
            self.sheet_attack_se = pygame.image.load("assets/Enemies/Attack/Enemy-Melee-Attack-SE.png").convert_alpha()
            self.sheet_attack_sw = pygame.image.load("assets/Enemies/Attack/Enemy-Melee-Attack-SW.png").convert_alpha()
            
            # Cargar sprite de muerte
            self.sheet_death = pygame.image.load("assets/Enemies/Death/Enemy-Melee-Death.png").convert_alpha()
            
            # Escalar sprites
            for sheet in [self.sheet_idle_n, self.sheet_idle_s, self.sheet_idle_e, self.sheet_idle_w,
                         self.sheet_idle_ne, self.sheet_idle_nw, self.sheet_idle_se, self.sheet_idle_sw,
                         self.sheet_attack_n, self.sheet_attack_s, self.sheet_attack_e, self.sheet_attack_w,
                         self.sheet_attack_ne, self.sheet_attack_nw, self.sheet_attack_se, self.sheet_attack_sw,
                         self.sheet_death]:
                sheet = pygame.transform.scale(sheet, self.SPRITE_SIZE)
        except pygame.error as e:
            print(f"Error al cargar los sprites: {e}")
            raise

    def _apply_color_tint(self, surface: pygame.Surface) -> pygame.Surface:
        """Aplica un tinte de color al sprite según el nivel del enemigo."""
        if self.level not in self.level_colors:
            return surface
            
        # Crear una superficie con el tinte
        tint = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        tint.fill(self.level_colors[self.level])
        
        # Combinar el sprite original con el tinte
        result = surface.copy()
        result.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return result

    def _get_initial_image(self) -> pygame.Surface:
        """Retorna la imagen inicial del enemigo."""
        try:
            image = self.sheet_idle_s.subsurface(pygame.Rect(0, 0, 32, 32))
            scaled_image = pygame.transform.scale(image, (self.SPRITE_SIZE[0] * self.SCALE_FACTOR, self.SPRITE_SIZE[1] * self.SCALE_FACTOR))
            return self._apply_color_tint(scaled_image)
        except pygame.error as e:
            print(f"Error al obtener la imagen inicial: {e}")
            surface = pygame.Surface(self.SPRITE_SIZE)
            surface.fill((255, 0, 0))
            return surface

    def _initialize_animation_states(self) -> dict:
        """Inicializa y retorna los estados de animación con sus respectivos frames y tamaños personalizados."""
        return {
            "idle": {
                "N": [(42, 55, 188, 164), (298, 55, 188, 164), (553, 55, 188, 164), (815, 55, 188, 164),
                      (1063, 55, 188, 164), (1345, 55, 188, 164), (1574, 55, 188, 164), (1848, 55, 188, 164),
                      (2078, 55, 188, 164), (2356, 55, 188, 164), (2606, 55, 188, 164), (2853, 55, 188, 164)],
                "S": [(40, 47, 151, 171), (301, 45, 151, 171), (529, 42, 151, 171), (794, 41, 151, 171),
                      (1048, 40, 151, 171), (1316, 40, 151, 171), (1571, 40, 151, 171), (1814, 43, 151, 171),
                      (2083, 38, 151, 171), (2335, 41, 151, 171), (2585, 45, 151, 171), (2835, 45, 151, 171)],
                "E": [(80, 50, 133, 186), (328, 49, 133, 186), (581, 47, 133, 186), (838, 45, 133, 186),
                      (1091, 47, 133, 186), (1350, 46, 133, 186), (1614, 48, 133, 186), (1867, 47, 133, 186),
                      (2122, 45, 133, 186), (2371, 45, 133, 186), (2625, 40, 133, 186), (2869, 46, 133, 186)],
                "W": [(83, 52, 125, 201), (327, 52, 125, 201), (569, 52, 125, 201), (836, 52, 125, 201),
                      (1087, 44, 125, 201), (1359, 52, 125, 201), (1613, 52, 125, 201), (1847, 52, 125, 201),
                      (2108, 52, 125, 201), (2366, 37, 125, 201), (2615, 33, 125, 201), (2880, 34, 125, 201)],
                "NE": [(72, 47, 171, 188), (311, 44, 171, 188), (550, 41, 171, 188), (830, 39, 171, 188),
                       (1060, 35, 171, 188), (1311, 31, 171, 188), (1601, 52, 171, 188), (1846, 52, 171, 188),
                       (2101, 51, 171, 188), (2364, 48, 171, 188), (2598, 47, 171, 188), (2866, 43, 171, 188)],
                "NW": [(62, 47, 145, 173), (316, 44, 145, 173), (567, 42, 145, 173), (805, 45, 145, 173),
                       (1069, 50, 145, 173), (1339, 46, 145, 173), (1597, 43, 145, 173), (1832, 43, 145, 173),
                       (2107, 42, 145, 173), (2359, 42, 145, 173), (2605, 40, 145, 173), (2855, 40, 145, 173)],
                "SE": [(100, 73, 152, 183), (305, 55, 152, 194), (562, 50, 152, 194), (807, 49, 152, 194),
                       (1067, 49, 152, 194), (1318, 49, 152, 194), (1571, 47, 152, 194), (1827, 47, 152, 194),
                       (2100, 47, 152, 194), (2355, 43, 152, 194), (2600, 46, 152, 194), (2856, 44, 152, 194)],
                "SW": [(62, 51, 177, 188), (310, 48, 177, 188), (558, 47, 177, 188), (808, 47, 177, 188),
                       (1068, 43, 177, 188), (1328, 49, 177, 188), (1588, 39, 177, 188), (1832, 40, 177, 188),
                       (2084, 39, 177, 188), (2340, 37, 177, 188), (2602, 37, 177, 188), (2854, 36, 177, 188)]
            },
            "attack": {
                "N": [(69,54,125,194), (325,56,125,194), (583,53,125,194), (842,53,125,194), (1096,46,125,194),
                      (1357,56,125,194), (1605,51,125,194), (1865,43,125,194), (2116,37,125,194), (2350,34,125,194)],
                "S": [(42,49,138,197), (279,44,138,197), (536,43,138,197), (808,40,138,197), (1064,39,138,197),
                      (1309,38,138,197), (1573,36,138,197), (1831,35,138,197), (2097,32,138,197), (2366,34,138,197)],
                "E": [(80,59,193,161), (341,57,193,161), (589,58,193,161), (851,56,193,161), (1111,55,193,161),
                      (1363,55,193,161), (1622,56,193,161), (1873,50,193,161), (2130,51,193,161), (2380,45,193,161)],
                "W": [(80,49,116,168), (346,45,116,168), (592,45,116,168), (852,42,116,168), (1095,50,116,168),
                      (1352,46,116,168), (1597,48,116,168), (1850,51,206,176), (2103,52,206,176), (2360,49,206,176)],
                "NE": [(73,54,176,202), (336,46,176,205), (594,51,176,203), (841,53,176,203), (1095,47,176,209),
                       (1349,53,176,203), (1600,57,176,199), (1843,48,176,208), (2090,55,176,201), (2338,48,176,208)],
                "NW": [(74,47,181,191), (327,49,181,191), (582,53,181,191), (841,57,181,191), (1101,54,181,191),
                       (1356,46,181,191), (1607,55,181,191), (1865,54,181,191), (2118,41,181,191), (2369,34,181,191)],
                "SE": [(53,48,199,171), (314,59,199,171), (571,57,199,171), (837,56,199,171), (1092,59,199,171),
                       (1368,57,199,171), (1618,54,199,171), (1879,49,199,171), (2129,55,199,171), (2381,50,199,171)],
                "SW": [(65,50,187,206), (304,45,187,208), (566,46,187,208), (821,43,187,208), (1078,41,187,208),
                       (1326,42,187,208), (1579,36,187,208), (1834,39,187,208), (2094,37,187,208), (2357,39,187,208)]
            },
            "death": {
                "default": [(36,46,144,161), (290,45,144,161), (551,46,144,161), (805,46,144,161),
                           (1057,42,144,161), (1315,48,144,161), (1570,44,144,164), (1825,50,144,161),
                           (2075,47,144,161), (2334,44,178,172), (2596,42,178,172), (2850,43,178,172)]
            }
        }

    def get_current_sheet(self) -> pygame.Surface:
        """Retorna la hoja de sprites actual según el estado y dirección del enemigo."""
        direction_mapping = {
            "N": "n",
            "S": "s",
            "E": "e",
            "W": "w",
            "NE": "ne",
            "NW": "nw",
            "SE": "se",
            "SW": "sw"
        }
        sheet_name = f"sheet_{self.state}_{direction_mapping[self.direction]}"
        return getattr(self, sheet_name)

    def _update_animation(self, dt: float) -> None:
        """Actualiza el frame de animación actual."""
        if not self.is_alive and not self.is_dying:
            self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
            return

        # Actualizar el timer de animación
        self.animation_timer += dt * 1000  # Convertir a milisegundos

        if self.state == "death":
            if self.is_dying:
                if self.animation_timer >= self.DEATH_ANIMATION_DELAY:
                    self.animation_timer = 0
                    self.death_frame += 1
                    if self.death_frame >= len(self.states[self.state]["default"]):
                        self.is_dying = False
                        self.is_dead = True
                        self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
                        if self._death_complete_callback:
                            self._death_complete_callback(self)
                        return
                # Asegurarse de que siempre se muestre un frame
                current_frame = self.states[self.state]["default"][min(self.death_frame, len(self.states[self.state]["default"]) - 1)]
                frame = self.sheet_death.subsurface(pygame.Rect(current_frame))
                if self.death_frame >= len(self.states[self.state]["default"]) - 2:
                    frame = pygame.transform.scale(frame, (45, 45))
                else:
                    frame = pygame.transform.scale(frame, (78, 93))
                self.image = self._apply_color_tint(frame)
            return

        if self.state == "attack":
            if self.is_attacking:
                if self.animation_timer >= self.animation_delay:
                    self.animation_timer = 0
                    self.attack_frame += 1
                    if self.attack_frame >= len(self.states[self.state][self.direction]):
                        self.is_attacking = False
                        self.attack_frame = 0
                        self.state = "idle"
                        self.animation_delay = self.ANIMATION_DELAY
            current_frame = self.states[self.state][self.direction][self.attack_frame if self.attack_frame < len(self.states[self.state][self.direction]) else -1]
            current_sheet = self.get_current_sheet()
            frame = current_sheet.subsurface(pygame.Rect(current_frame))
            frame = pygame.transform.scale(frame, (78, 93))
            self.image = self._apply_color_tint(frame)
            return

        # Animación normal (idle)
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.frame = (self.frame + 1) % len(self.states[self.state][self.direction])
            current_frame = self.states[self.state][self.direction][self.frame]
            current_sheet = self.get_current_sheet()
            frame = current_sheet.subsurface(pygame.Rect(current_frame))
            frame = pygame.transform.scale(frame, (78, 93))
            self.image = self._apply_color_tint(frame)

    def _update_direction(self, dx: float, dy: float) -> None:
        """Actualiza la dirección del enemigo basado en el movimiento."""
        if dx == 0 and dy == 0:
            return

        angle = atan2(dy, dx)
        angle_deg = angle * 180 / 3.14159

        if -22.5 <= angle_deg < 22.5:
            self.direction = "E"
        elif 22.5 <= angle_deg < 67.5:
            self.direction = "SE"
        elif 67.5 <= angle_deg < 112.5:
            self.direction = "S"
        elif 112.5 <= angle_deg < 157.5:
            self.direction = "SW"
        elif 157.5 <= angle_deg < 180 or -180 <= angle_deg < -157.5:
            self.direction = "W"
        elif -157.5 <= angle_deg < -112.5:
            self.direction = "NW"
        elif -112.5 <= angle_deg < -67.5:
            self.direction = "N"
        elif -67.5 <= angle_deg < -22.5:
            self.direction = "NE"

    def update(self, dt: float, player, map_obj):
        """Actualiza el estado del enemigo."""
        if not self.is_alive and not self.is_dying:
            return

        # No actualizar si está cargando
        if self._is_loading:
            return

        # Actualizar cooldown de ataque
        if self._current_cooldown > 0:
            self._current_cooldown -= dt

        # Actualizar knockback si está activo
        if self._knockback_active:
            self._update_knockback(dt, map_obj)
        elif not self.is_dying:  # Solo mover si no está muriendo
            # Movimiento normal hacia el jugador
            self._move_towards_player(dt, player, map_obj)

        # Intentar atacar si está en rango y no está muriendo
        if not self.is_dying and self._can_attack(player):
            self._attack(player)

        # Actualizar animación
        self._update_animation(dt)

    def _move_towards_player(self, dt: float, player, map_obj):
        """Mueve al enemigo hacia el jugador."""
        dx = player.x - self.x
        dy = player.y - self.y

        if dx != 0 or dy != 0:
            # Calcular la distancia
            distance = (dx**2 + dy**2)**0.5
            
            # Si estamos muy cerca del jugador, mantener una distancia mínima
            if distance < self.attack_range:
                # Calcular dirección opuesta al jugador
                if distance > 0:  # Evitar división por cero
                    dx = -dx / distance
                    dy = -dy / distance
                    new_x = self.x + dx * self.speed * dt
                    new_y = self.y + dy * self.speed * dt
                    
                    # Intentar movimiento en X
                    if dx != 0 and self._can_move_to(new_x, self.y, map_obj):
                        self.x = new_x
                    
                    # Intentar movimiento en Y
                    if dy != 0 and self._can_move_to(self.x, new_y, map_obj):
                        self.y = new_y
                return
            
            # Movimiento normal hacia el jugador
            new_x = self.x + (dx/distance) * self.speed * dt
            new_y = self.y + (dy/distance) * self.speed * dt

            # Actualizar dirección basada en el movimiento
            self._update_direction(dx, dy)

            # Intentar movimiento en X
            if dx != 0 and self._can_move_to(new_x, self.y, map_obj):
                self.x = new_x

            # Intentar movimiento en Y
            if dy != 0 and self._can_move_to(self.x, new_y, map_obj):
                self.y = new_y

    def _attack(self, player):
        """Realiza un ataque al jugador."""
        if not self.is_attacking:
            self.state = "attack"
            self.is_attacking = True
            self.attack_frame = 0
            self.animation_delay = self.ATTACK_ANIMATION_DELAY
            player.take_damage(self.damage)
            self._current_cooldown = self.attack_cooldown

    def take_damage(self, damage: float):
        """El enemigo recibe daño."""
        if self.is_dying or self.is_dead:
            return
            
        super().take_damage(damage)
        if not self.is_alive:
            self.state = "death"
            self.is_dying = True
            self.death_frame = 0
            self.animation_timer = 0
            self.animation_delay = self.DEATH_ANIMATION_DELAY
            # Iniciar la generación de nuevos enemigos inmediatamente
            if self._death_complete_callback:
                self._death_complete_callback(self)
            # Asegurarse de que la primera frame de muerte se muestre inmediatamente
            current_frame = self.states[self.state]["default"][0]
            frame = self.sheet_death.subsurface(pygame.Rect(current_frame))
            frame = pygame.transform.scale(frame, (78, 93))
            self.image = self._apply_color_tint(frame)

    def _update_knockback(self, dt: float, map_obj):
        """Actualiza el estado del knockback."""
        current_time = time.time()
        elapsed_time = current_time - self._knockback_start_time
        
        if elapsed_time >= CONFIG['knockback']['duration']:
            self._knockback_active = False
            self._knockback_velocity = (0.0, 0.0)
            return
            
        # Calcular la velocidad actual con fricción
        friction = CONFIG['knockback']['friction']
        vx = self._knockback_velocity[0] * friction
        vy = self._knockback_velocity[1] * friction
        
        # Calcular nueva posición
        new_x = self.x + vx * dt
        new_y = self.y + vy * dt
        
        # Verificar colisiones con el mapa
        if self._can_move_to(new_x, self.y, map_obj):
            self.x = new_x
        else:
            vx = 0
            
        if self._can_move_to(self.x, new_y, map_obj):
            self.y = new_y
        else:
            vy = 0
            
        # Actualizar velocidad
        self._knockback_velocity = (vx, vy)
            
    def _can_move_to(self, new_x: float, new_y: float, map_obj) -> bool:
        """Verifica si el enemigo puede moverse a la nueva posición."""
        enemy_hitbox = Hitbox(new_x, new_y, self.width, self.height)
        min_x = floor(new_x)
        max_x = ceil(new_x + self.width - 1e-6)
        min_y = floor(new_y)
        max_y = ceil(new_y + self.height - 1e-6)
        
        try:
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    wall_hitbox = map_obj.get_wall_hitbox(x, y)
                    if wall_hitbox and enemy_hitbox.collides_with(wall_hitbox):
                        return False
        except IndexError:
            return False
        return True
        
    def _can_attack(self, player) -> bool:
        """Verifica si el enemigo puede atacar al jugador."""
        if self._current_cooldown > 0 or self._knockback_active:
            return False
            
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2)**0.5
        
        return distance <= self.attack_range

    def check_attack_hit(self, attack) -> bool:
        """Verifica si el enemigo está dentro del rango de un ataque."""
        if not attack.is_executing:
            return False
            
        # Calcular el centro del enemigo
        center_x = self.x + (self.width / 2)
        center_y = self.y + (self.height / 2)
        
        # Verificar si está en rango
        if attack.is_in_range(center_x, center_y):
            # Calcular daño
            damage = attack.calculate_damage()
            self.take_damage(damage)
            
            # Calcular dirección del knockback (opuesta a la dirección del enemigo hacia el jugador)
            dx = center_x - attack._source_x
            dy = center_y - attack._source_y
            
            # Normalizar el vector
            length = sqrt(dx*dx + dy*dy)
            if length > 0:
                knockback_dir = (dx/length, dy/length)
                
                # Iniciar knockback
                self._knockback_active = True
                self._knockback_start_time = time.time()
                self._knockback_direction = knockback_dir
                self._knockback_force = attack.knockback
                
                # Calcular velocidad inicial
                initial_speed = self._knockback_force * 2  # Factor de velocidad inicial
                self._knockback_velocity = (
                    knockback_dir[0] * initial_speed,
                    knockback_dir[1] * initial_speed
                )
                
            return True
            
        return False
