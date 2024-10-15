from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from algorithms.GilbertMooreEncoder import GilbertMooreEncoder
from widgets.BaseTab import BaseTab


class GilbertMooreTab(BaseTab):
    ENCODER = GilbertMooreEncoder
    def __init__(self, parent=None):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("У данного алгоритма нет настроек", self)

        layout.addWidget(label)
        self.setLayout(layout)