import csv
import re

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QTabWidget, QTableView, QAction, QMessageBox, \
    QFileDialog, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QLabel

from windows.AboutWindow import AboutWindow

from algorithms.GilbertMooreEncoder import GilbertMooreEncoder

def prepare_additional_text(encoder, input=None, output=None):
    result = str(encoder)
    if input is not None and output is not None:
        result += "\n" + ("-" * 50) + "\n"
        result += f"Ввод: {input}\n"
        result += f"Вывод: {output}\n"
    return result

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.probabilities = dict()
        self.encoder = None

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
        self.sequence_input.setDisabled(True)
        self.sequence_input.setPlaceholderText("Введите последовательность")

        self.encoded_sequence_input = QLineEdit()
        self.encoded_sequence_input.setDisabled(True)
        self.encoded_sequence_input.setPlaceholderText("Введите закодированную последовательность")
        regex_pattern = f"^[10]+;"
        regexp = QtCore.QRegExp(regex_pattern)
        validator = QtGui.QRegExpValidator(regexp)
        self.encoded_sequence_input.setValidator(validator)

        self.encode_button = QPushButton("Кодировать")
        self.encode_button.setDisabled(True)
        self.encode_button.clicked.connect(self.encode)
        self.decode_button = QPushButton("Декодировать")
        self.decode_button.setDisabled(True)
        self.decode_button.clicked.connect(self.decode)


        task_1_tab_layout.addWidget(self.sequence_input)
        task_1_tab_layout.addWidget(self.encoded_sequence_input)
        task_1_tab_layout.addWidget(self.encode_button)
        task_1_tab_layout.addWidget(self.decode_button)

        task_1_tab.setLayout(task_1_tab_layout)

        tab_widget = QTabWidget()
        tab_widget.addTab(task_1_tab, "Алгоритм Гильбера-Мура")
        layout.addWidget(tab_widget)
        self.additional_info_field = QTextEdit()
        self.additional_info_field.setText(
            "1. Выберите файл алфавита и вероятностей\n2. Введите последовательность\n3. нажмите на кодировать или декодировать")
        self.additional_info_field.setReadOnly(True)
        layout.addWidget(self.additional_info_field)

        # Устанавливаем компоновку для центрального виджета
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.statusBar().showMessage("Выберете файл алфавита и вероятностей")

    def create_menu(self):
        menubar = self.menuBar()

        # Создание меню "Файл"
        file_menu = menubar.addMenu("Файл")

        # Пункты меню в "Файл"
        import_probs_action = QAction("Импортировать алфавит и вероятности", self)
        import_sequence_action = QAction("Импортировать последовательностей", self)
        self.export_answer_action = QAction("Экспортировать ответ", self)
        self.export_answer_action.setDisabled(True)

        import_probs_action.triggered.connect(self.import_probabilities)
        self.export_answer_action.triggered.connect(self.export_answer)
        import_sequence_action.triggered.connect(self.import_sequence)

        file_menu.addAction(import_probs_action)
        file_menu.addAction(import_sequence_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_answer_action)

        # Создание меню "О нас"
        about_action = QAction("О программе", self)
        menubar.addAction(about_action)

        about_action.triggered.connect(self.show_about_window)

    def decode(self):
        try:
            text = self.encoded_sequence_input.text()
            decoded_message = self.encoder.decode(text)
            self.additional_info_field.setText(prepare_additional_text(self.encoder, text, decoded_message))
            self.sequence_input.setText(decoded_message)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка декодирования!", f"Во время декодирования произошла ошибка '{e}'")

    def encode(self):
        try:
            text = self.sequence_input.text()
            encoded_message = self.encoder.encode(text)
            self.additional_info_field.setText(prepare_additional_text(self.encoder, text, encoded_message))
            self.encoded_sequence_input.setText(encoded_message)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка кодирования!", f"Во время кодирования произошла ошибка '{e}'")

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
                self.statusBar().showMessage(f"Вероятности успешно импортированы из {file_name}.")
                self.sequence_input.setDisabled(False)
                self.encoded_sequence_input.setDisabled(False)
                self.encode_button.setDisabled(False)
                self.decode_button.setDisabled(False)
                self.export_answer_action.setDisabled(False)
                regex_pattern = f"^[{''.join(map(re.escape, self.probabilities.keys()))}]+;"
                regexp = QtCore.QRegExp(regex_pattern)
                validator = QtGui.QRegExpValidator(regexp)
                self.sequence_input.setValidator(validator)
                self.encoder = GilbertMooreEncoder(self.probabilities)
                self.additional_info_field.setText(prepare_additional_text(self.encoder))
            except Exception as e:
                QMessageBox.critical(self, "Ошибка импорта!", f"Во время импорта произошла ошибка '{e}'")

    def import_sequence(self):
        # Диалог для выбора файла (импорт вероятностей)
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл c последовательностью", "",
                                                   "Text Files (*.txt)")
        if file_name:
            try:
                with open(file_name, mode="r") as file:
                    self.sequence_input.setText(file.readline().strip())
                self.statusBar().showMessage(f"Последовательность успешно импортирована из {file_name}.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка импорта!", f"Во время импорта произошла ошибка '{e}'")

    def export_answer(self):
        # Диалог для сохранения файла (экспорт ответа)
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить ответ", "", "Text Files (*.txt)")
        if file_name:
            try:
                with open(file_name, mode="w", encoding="utf-8") as file:
                    print(self.additional_info_field.toPlainText(), file=file)
                self.statusBar().showMessage(f"Ответ успешно экспортирован в {file_name}.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка импорта!", f"Во время импорта произошла ошибка '{e}'")

    def show_about_window(self):
        # Открытие окна "О нас"
        self.about_window = AboutWindow()
        self.about_window.show()
