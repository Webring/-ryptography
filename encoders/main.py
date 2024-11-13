import sys

from PyQt5.QtWidgets import QApplication
from windows.MainWindow import MainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    sys.excepthook = except_hook

    app = QApplication(sys.argv)  # Передача аргументов

    window = MainWindow()  # Инициализация окна
    window.show()  # Показ окна

    sys.exit(app.exec_())  # Сигнал о закрытии
