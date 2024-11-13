from PyQt5.QtWidgets import QWidget


class BaseTab(QWidget):
    def __init__(self):
        self.encoder = None
        super().__init__()

    def update_encoder(self, probs: dict):
        self.encoder = self.ENCODER(probs)