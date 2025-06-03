class PauseMenuModel:
    def __init__(self):
        self.title = "PAUSA"
        self.button_labels = ["Continuar", "Salir al Menú"]
        self.selected_option = None

    def get_title(self):
        return self.title

    def get_button_labels(self):
        return self.button_labels

    def set_selected_option(self, option_label):
        self.selected_option = option_label