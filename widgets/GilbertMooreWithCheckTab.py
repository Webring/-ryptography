from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from algorithms.GilbertMooreEncoderWithCheck import GilbertMooreEncoderWithCheck
from widgets.BaseTab import BaseTab


class GilbertMooreWithCheckersTab(BaseTab):
    ENCODER = GilbertMooreEncoderWithCheck
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("У данного алгоритма нет настроек", self)

        layout.addWidget(label)
        self.setLayout(layout)