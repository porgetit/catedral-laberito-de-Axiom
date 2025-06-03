# controller.py
import pygame
import sys

class MenuController:
    def __init__(self, model):
        self.model = model
        self.running = True

    def handle_event(self, event, button_rects):
        if event.type == pygame.QUIT:
            self.running = False
            return "Salir" # Devolver la acción para que main.py la maneje

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Click izquierdo
                mouse_pos = event.pos
                button_labels = self.model.get_button_labels()
                
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        selected_label = button_labels[i]
                        self.model.set_selected_option(selected_label)
                        return self.perform_action(selected_label)
        return None

    def perform_action(self, action_label):
        # Aquí defines qué hace cada botón
        if action_label == "Jugar":
            print(f"Acción: Iniciar el juego...")
            # Aquí llamarías a la lógica para iniciar el juego
        elif action_label == "Puntajes":
            return "Puntajes"
            # Aquí mostrarías la pantalla de puntajes
        elif action_label == "Controles":
            print(f"Acción: Mostrar controles...")
        elif action_label == "Créditos":
            print(f"Acción: Mostrar créditos...")
        elif action_label == "Salir":
            print(f"Acción: Saliendo del juego...")
            self.running = False
            return "Salir" # Señal para que el bucle principal termine
        return action_label # Devolver la etiqueta de la acción para posible manejo externo