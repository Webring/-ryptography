from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("О нас")

        layout = QVBoxLayout()
        label = QLabel(
            " Данная программа реализует алгоритмы генерации простых чисел\n "
            "Алгоритм пробных делений пробегается по всем числам от 2 до корень(n)\n"
            "и проверят делители этого числа с теми, что есть в этом диапазоне.\n"
            "Решето Эратосфена задаёт последовательность всех простых чисел\n"
            "от 2 до числа n, где n-простое число.\n\n"
            "Авторы: Васильев Михаил, Серов Виктор, Горбунова Алена", self)

        layout.addWidget(label)
        self.setLayout(layout)
