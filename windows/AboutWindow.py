from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("О нас")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()
        label = QLabel("Это окно 'О нас'.\nАвтор: И. Иванов.\nВерсия: 1.0", self)
        layout.addWidget(label)
        self.setLayout(layout)