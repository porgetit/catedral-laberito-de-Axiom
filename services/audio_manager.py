import pygame
from services.config import CONFIG

class AudioManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa el sistema de audio."""
        pygame.mixer.init()
        self.menu_music = pygame.mixer.Sound("sound/menu.mp3")
        self.coliseo_music = pygame.mixer.Sound("sound/coliseo.mp3")
        self.attack_sound = pygame.mixer.Sound("sound/ataque.mp3")
        
        # Configurar volúmenes
        self.menu_music.set_volume(0.7)  # 70% del volumen máximo
        self.coliseo_music.set_volume(0.4)  # 40% del volumen máximo
        self.attack_sound.set_volume(0.8)  # 80% del volumen máximo

    def play_menu_music(self):
        """Reproduce la música del menú."""
        self.stop_all()
        self.menu_music.play(-1)  # -1 para reproducir en loop

    def play_coliseo_music(self):
        """Reproduce la música del coliseo."""
        self.stop_all()
        self.coliseo_music.play(-1)  # -1 para reproducir en loop

    def play_attack_sound(self):
        """Reproduce el sonido de ataque."""
        self.attack_sound.play()

    def stop_all(self):
        """Detiene todos los sonidos."""
        pygame.mixer.stop()

    def pause_all(self):
        """Pausa todos los sonidos."""
        pygame.mixer.pause()

    def unpause_all(self):
        """Reanuda todos los sonidos."""
        pygame.mixer.unpause() 