# model.py

class MenuModel:
    def __init__(self):
        self.title = "Coliseo de Axiom"
        self.button_labels = ["Jugar", "Puntajes", "Controles", "Créditos", "Salir"]
        self.selected_option = None # Podría usarse para saber qué opción se eligió
        # En un juego más complejo, aquí iría el estado del juego, puntajes, etc.

    def get_title(self):
        return self.title

    def get_button_labels(self):
        return self.button_labels

    def set_selected_option(self, option_label):
        self.selected_option = option_label