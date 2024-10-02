import sys

from PyQt5.QtWidgets import QApplication
from windows.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv) # Передача аргументов

    window = MainWindow() # Инициализация окна
    window.show() # Показ окна

    sys.exit(app.exec_()) # Сигнал о закрытии
