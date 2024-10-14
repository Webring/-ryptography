from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from algorithms.Hamming import HammingCode


class GilbertMooreTab(QWidget):
    ENCODER = HammingCode
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        errors_to_file_button = QPushButton("Записать ошибки в файл", self)

        layout.addWidget(errors_to_file_button)
        self.setLayout(layout)