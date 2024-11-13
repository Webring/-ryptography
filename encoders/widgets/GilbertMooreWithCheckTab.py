from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QFileDialog

from algorithms.GilbertMooreEncoderWithCheck import GilbertMooreEncoderWithCheck
from widgets.BaseTab import BaseTab


class GilbertMooreWithCheckersTab(BaseTab):
    ENCODER = GilbertMooreEncoderWithCheck
    def __init__(self, parent=None):
        super().__init__()
        layout = QVBoxLayout()
        # label = QLabel("У данного алгоритма нет настроек", self)
        errors_to_file_button = QPushButton("Записать ошибки в файл", self)
        errors_to_file_button.clicked.connect(self.write_errors)

        # layout.addWidget(label)
        layout.addWidget(errors_to_file_button)
        self.setLayout(layout)

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