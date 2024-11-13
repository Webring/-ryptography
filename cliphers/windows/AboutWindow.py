from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("О нас")

        layout = QVBoxLayout()
        label = QLabel("Программа ...\n\n"
                       "Авторы: Васильев Михаил, Серов Виктор, Горбунова Алена", self)

        layout.addWidget(label)
        self.setLayout(layout)