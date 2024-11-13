from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("О нас")

        layout = QVBoxLayout()
        label = QLabel("Программа осуществляет работу нелинейного конгруэнтного\n"
                       "генератора Ейхенауэра-Лена с обращением.\n"
                       "Параметры на входе:\n"
                       "- N - мощность алфавита (N = 2^q)\n"
                       "- a - ненулевой множитель (а - нечётное)\n"
                       "- с - смещение (с - чётное)\n"
                       "- x0 - начальное значение (x0 - нечётное)\n\n"
                       "Авторы: Васильев Михаил, Серов Виктор, Горбунова Алена", self)

        layout.addWidget(label)
        self.setLayout(layout)