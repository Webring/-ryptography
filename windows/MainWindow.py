import csv

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QTabWidget, QTableView, QAction, QMessageBox, \
    QFileDialog, QLineEdit, QPushButton, QVBoxLayout

from windows.AboutWindow import AboutWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.sequence = ""
        self.probabilities = dict()

        # Настройка окна
        self.setWindowTitle("Криптография")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.initUI()
        self.create_menu()


    def initUI(self):
        # Основной виджет и компоновка
        central_widget = QWidget()
        layout = QHBoxLayout()

        task_1_tab = QWidget()
        task_1_tab_layout = QVBoxLayout()
        self.sequence_input = QLineEdit()
        self.encode_button = QPushButton("Кодировать")
        self.decode_button = QPushButton("Декодировать")
        task_1_tab_layout.addWidget(self.sequence_input)
        task_1_tab_layout.addWidget(self.encode_button)
        task_1_tab_layout.addWidget(self.decode_button)

        task_1_tab.setLayout(task_1_tab_layout)

        tab_widget = QTabWidget()
        tab_widget.addTab(task_1_tab, "Первая лаба")
        layout.addWidget(tab_widget)
        layout.addWidget(QTableView())

        # Устанавливаем компоновку для центрального виджета
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_menu(self):
        menubar = self.menuBar()

        # Создание меню "Файл"
        file_menu = menubar.addMenu("Файл")

        # Пункты меню в "Файл"
        import_probs_action = QAction("Импортировать алфавит и вероятности", self)
        import_sequence_action = QAction("Импортировать последовательностей", self)

        export_answer_action = QAction("Экспортировать ответ", self)

        import_probs_action.triggered.connect(self.import_probabilities)
        export_answer_action.triggered.connect(self.export_answer)
        import_sequence_action.triggered.connect(self.import_sequence)

        file_menu.addAction(import_probs_action)
        file_menu.addAction(import_sequence_action)
        file_menu.addAction(export_answer_action)

        # Создание меню "О нас"
        about_action = QAction("О нас", self)
        menubar.addAction(about_action)

        about_action.triggered.connect(self.show_about_window)


    def import_probabilities(self):
        # Диалог для выбора файла (импорт вероятностей)
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл с вероятностями", "",
                                                   "Text Files (*.csv)")
        if file_name:
            try:
                with open(file_name, mode="r") as file:
                    reader = csv.reader(file, delimiter=';')
                    for row in reader:
                        symbol, prob = row
                        self.probabilities[symbol] = float(prob)
                QMessageBox.information(self, "Импорт вероятностей", f"Вероятности успешно импортированы из {file_name}.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка импорта!", f"Во время импорта произошла ошибка '{e}'")
    def import_sequence(self):
        # Диалог для выбора файла (импорт вероятностей)
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл c последовательностью", "",
                                                   "Text Files (*.txt)")
        if file_name:
            try:
                with open(file_name, mode="r") as file:
                    self.sequence = file.readline().strip()
                self.sequence_input.setText(self.sequence)
                QMessageBox.information(self, "Импорт последовательности", f"Последовательность успешно импортирована из {file_name}.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка импорта!", f"Во время импорта произошла ошибка '{e}'")

    def export_answer(self):
        # Диалог для сохранения файла (экспорт ответа)
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить ответ", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            # Логика экспорта ответа
            QMessageBox.information(self, "Экспорт", f"Ответ успешно экспортирован в {file_name}.")

    def show_about_window(self):
        # Открытие окна "О нас"
        self.about_window = AboutWindow()
        self.about_window.show()
