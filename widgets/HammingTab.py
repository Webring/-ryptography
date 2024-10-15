import csv

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox

from algorithms.HammingEncoder import HammingEncoder
from widgets.BaseTab import BaseTab


class HammingTab(BaseTab):
    ENCODER = HammingEncoder
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        load_hemming_matrix_button = QPushButton("Загрузить матрицу хемминга", self)
        load_hemming_matrix_button.clicked.connect(self.load_hemming_matrix)

        errors_to_file_button = QPushButton("Записать ошибки в файл", self)
        errors_to_file_button.clicked.connect(self.write_errors)

        layout.addWidget(load_hemming_matrix_button)
        layout.addWidget(errors_to_file_button)
        self.setLayout(layout)

    def load_hemming_matrix(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Загрузить файл матрицы Хэмминга", "", "CSV Files (*.csv)")

        if file_name:
            try:
                # Открываем и загружаем файл CSV
                with open(file_name, newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=';')
                    self.encoder.read_hamming_matrix([list(map(int, row)) for row in reader])

                QMessageBox.information(self, "Успех", "Матрица Хэмминга успешно загружена.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить матрицу: {str(e)}")

    def write_errors(self):

        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл с ошибками", "", "Текстовый файл (*.txt)")

        if file_name:
            try:
                # Генерируем фейковые данные ошибок (замените на реальные расчеты)
                errors = self.encoder.errors or "Ошибок нет"

                # Записываем ошибки в CSV файл
                with open(file_name, mode='w', encoding="utf-8") as file:
                    print(errors, sep="\n", file=file)

                QMessageBox.information(self, "Успех", "Ошибки успешно записаны в файл.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось записать ошибки: {str(e)}")


