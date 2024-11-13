# Импорт необходимых модулей из библиотеки PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QAction, QMessageBox, \
    QFileDialog, QPushButton, QVBoxLayout, QTextEdit, QLabel, QSpinBox

from cliphers.algorithms.EichenauerLehnGeneratorWithReversal import EichenauerLehnGeneratorWithReversal
from cliphers.windows.AboutWindow import AboutWindow


def widget_with_label(widget, label: str):
    layout = QHBoxLayout()
    layout.addWidget(QLabel(label))
    layout.addWidget(widget)
    return layout


class MainWindow(QMainWindow):
    def __init__(self):
        # Инициализация главного окна
        super().__init__()

        # Настройка параметров окна
        self.setWindowTitle("Криптография")  # Устанавливаем заголовок окна
        self.setWindowIcon(QtGui.QIcon('icon.png'))  # Устанавливаем иконку окна
        self.initUI()  # Инициализируем пользовательский интерфейс
        self.create_menu()  # Создаем меню

    def initUI(self):
        # Создание основного виджета и его компоновки
        central_widget = QWidget()  # Основной виджет окна
        layout = QHBoxLayout()  # Горизонтальная компоновка элементов

        # Поле для вывода дополнительной информации
        tab_layout = QVBoxLayout()

        self.n_spin_box = QSpinBox()
        self.n_spin_box.setMinimum(1)
        self.a_spin_box = QSpinBox()
        self.c_spin_box = QSpinBox()
        self.x0_spin_box = QSpinBox()
        generate_button = QPushButton("Сгененировать")
        generate_button.clicked.connect(self.generate)

        tab_layout.addLayout(widget_with_label(self.n_spin_box, "N"))
        tab_layout.addLayout(widget_with_label(self.a_spin_box, "a"))
        tab_layout.addLayout(widget_with_label(self.c_spin_box, "c"))
        tab_layout.addLayout(widget_with_label(self.x0_spin_box, "x_0"))
        tab_layout.addWidget(generate_button)

        layout.addLayout(tab_layout)
        self.additional_info_field = QTextEdit()  # Поле для вывода информации
        self.additional_info_field.setText(
            "Введите коэффициенты со следующими ограничениями:\nN   – натуральное число, степень двойки\na   – неотрицательное нечетное целое число\nc   – неотрицательное четное целое число\nx0 – неотрицательное нечетное целое число")
        self.additional_info_field.setReadOnly(True)
        layout.addWidget(self.additional_info_field)

        # Устанавливаем компоновку для центрального виджета
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет
        self.statusBar().showMessage("Введите коэфиценты или импортируйте их из файла")  # Сообщение в статусной строке

    def create_menu(self):
        # Создание меню в верхней части окна
        menubar = self.menuBar()

        # Создание меню "Файл"
        file_menu = menubar.addMenu("Файл")

        self.import_data_action = QAction("Импортировать данные", self)
        self.export_answer_action = QAction("Экспортировать ответ", self)
        self.export_answer_action.triggered.connect(self.export_answer)
        self.import_data_action.triggered.connect(self.import_data)

        file_menu.addAction(self.import_data_action)
        file_menu.addAction(self.export_answer_action)

        about_menu = menubar.addMenu("О программе")
        about_action = QAction("О программе и Авторы", self)
        about_menu.addAction(about_action)

        about_action.triggered.connect(self.show_about_window)

    def import_data(self):
        # Экспорт закодированного/декодированного сообщения в файл
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл с данными", "", "Text Files (*.txt)")
        if file_name:
            coefs_line = ""
            try:
                with open(file_name, mode="r", encoding="utf-8") as file:
                    coefs_line = file.readline().strip()
                n, a, c, x0 = list(map(int, coefs_line.split()))
                self.n_spin_box.setValue(n)
                self.a_spin_box.setValue(a)
                self.c_spin_box.setValue(c)
                self.x0_spin_box.setValue(x0)
                self.statusBar().showMessage(f"Ответ успешно импортирован в {file_name}.")  # Обновляем статус
                self.generate()
            except Exception as e:
                # Отображаем сообщение об ошибке
                QMessageBox.critical(self, "Ошибка импорта!", f"Во время импорта произошла ошибка '{e}'")

    def export_answer(self):
        # Экспорт закодированного/декодированного сообщения в файл
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить ответ", "", "Text Files (*.txt)")
        if file_name:
            try:
                with open(file_name, mode="w", encoding="utf-8") as file:
                    print(self.additional_info_field.toPlainText(), file=file)  # Сохраняем текст
                self.statusBar().showMessage(f"Ответ успешно экспортирован в {file_name}.")  # Обновляем статус
            except Exception as e:
                # Отображаем сообщение об ошибке
                QMessageBox.critical(self, "Ошибка экспорта!", f"Во время экспорта произошла ошибка '{e}'")

    def generate(self):
        n = self.n_spin_box.value()
        a = self.a_spin_box.value()
        c = self.c_spin_box.value()
        x0 = self.x0_spin_box.value()

        try:
            generator = EichenauerLehnGeneratorWithReversal(n, a, c, x0)
            generator.run_generation()
            self.additional_info_field.setText(str(generator))
        except Exception as e:
            # Отображаем сообщение об ошибке
            QMessageBox.critical(self, "Ошибка генерации!", f"{e}")

    def show_about_window(self):
        # Открытие окна "О программе"
        self.about_window = AboutWindow()
        self.about_window.show()  # Показываем окно
