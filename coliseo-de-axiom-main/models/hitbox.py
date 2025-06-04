import pygame

class Hitbox:
    def __init__(self, x: float, y:float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    @property
    def rect(self) -> pygame.Rect:
        """Devuelve el rectángulo de la hitbox en coordenadas lógicas."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def collides_with(self, other: 'Hitbox') -> bool:
        """Comprueba si esta hitbox colisiona con otra."""
        return self.rect.colliderect(other.rect)

    def get_scaled_rect(self, scale: int) -> pygame.Rect:
        """Devuelve el rectángulo de la hitbox escalado a píxeles."""
        return pygame.Rect(
            int(self.x * scale),
            int(self.y * scale),
            int(self.width * scale),
            int(self.height * scale)
        )