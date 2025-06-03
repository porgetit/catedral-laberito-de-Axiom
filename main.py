"""Punto de entrada del juego."""
import pygame
from controllers.app_controller import AppController
from services.config import CONFIG

def run():
    pygame.init()
    screen = pygame.display.set_mode((CONFIG["window"]['width'], CONFIG["window"]['height']))
    pygame.display.set_caption(CONFIG["window"]['title'])
    clock = pygame.time.Clock()

    app = AppController(screen)
    running = True

    while running:
        dt = clock.tick(CONFIG["window"]['fps']) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # El controlador ahora retorna False si debe terminar
            if not app.handle_event(event):
                running = False

        if running:
            app.update(dt)
            app.render()

    pygame.quit()

if __name__ == "__main__":
    run()
