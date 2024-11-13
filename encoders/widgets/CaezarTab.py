from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSpinBox

from algorithms.CaezarEncoder import CaezarEncoder
from widgets.BaseTab import BaseTab


class CaezerTab(BaseTab):
    ENCODER = CaezarEncoder
    def __init__(self, parent=None):
        super().__init__()
        layout = QHBoxLayout()
        label = QLabel("Сдвиг", self)
        self.spinbox = QSpinBox(self)
        self.spinbox.valueChanged.connect(self.change_shift)

        layout.addWidget(label)
        layout.addWidget(self.spinbox)
        self.setLayout(layout)

    def update_encoder(self, probs: dict):
        super().update_encoder(probs)
        probs_len = len(probs)
        self.spinbox.setRange(min(1, probs_len), probs_len)


    def change_shift(self, value):
        self.encoder.set_shift(value)