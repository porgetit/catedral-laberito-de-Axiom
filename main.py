
"""Punto de entrada del juego.

Inicia PyGame, construye el AppController y empieza el bucle principal.
"""
import pygame
from controllers.app_controller import AppController

def run():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("The Game")
    clock = pygame.time.Clock()

    app = AppController(screen)

    running = True
    while running:
        dt = clock.tick(60) / 1000  # Delta time en segundos (frame rate fijo 60 FPS aprox.)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            app.handle_event(event)

        app.update(dt)
        app.render()

    pygame.quit()

if __name__ == "__main__":
    run()
