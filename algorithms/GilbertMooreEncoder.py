import math
from fractions import Fraction


class GilbertMooreEncoder:

    def __init__(self, probs: dict):
        """
        Конструктор класса. Принимает словарь, в котором ключи — это символы, а значения — их вероятности (в виде строк).
        """
        self.probs = probs
        # Проверяем, что сумма вероятностей равна 1. Если нет, выбрасывается исключение.
        if sum(map(lambda x: float(Fraction(x)), probs.values())) != 1:
            raise Exception("Сумма вероятностей не равна 1")
        self.probs = {key:value for key, value in probs.items() if float(Fraction(value)) != 0.0}

        self.codes_for_symbols = {}  # Словарь для хранения кодов для каждого символа.
        q, sigma, length, sum_of_lengths, entropy, self.components_of_Kraft = 0, 0, 0, 0, 0, 0

        # Проходим по каждому символу в словаре с вероятностями.
        for i in self.probs.keys():
            # Вычисляем энтропию для символа.
            entropy -= float(Fraction(self.probs[i])) * math.log(float(Fraction(self.probs[i])), 2)

            # Определяем промежуточное значение sigma.
            sigma = q + float(Fraction(self.probs[i])) / 2
            q += float(Fraction(self.probs[i]))

            # Определяем длину кода для текущего символа.
            length = int((-math.log(float(Fraction(self.probs[i])) / 2, 2)) + 0.999999)

            # Увеличиваем сумму длин для подсчета средней длины.
            sum_of_lengths += length

            # Преобразуем sigma в двоичное представление с заданной длиной.
            number_in_binary = self.decimal_to_binary_float(sigma, length)

            # Записываем двоичный код символа.
            self.codes_for_symbols[i] = number_in_binary

            # Проверяем неравенство Крафта.
            self.components_of_Kraft += 2 ** (-length)

        # Рассчитываем среднюю длину кода.
        self.average_length = sum_of_lengths / len(probs)

        # Рассчитываем избыточность.
        self.redundancy = self.average_length - entropy

    def __repr__(self):
        """
        Метод для представления объекта.
        """
        return f'Gilber-Murr({self.probs, self.result})'

    def __str__(self):
        """
        Метод для форматированного вывода информации о кодировании.
        """
        return f'''Алгоритм Гилберта-Мура
{'\n'.join([f'Символ: \'{key}\' кодируется \'{value}\'' for key, value in self.codes_for_symbols.items()])}
Средняя длина: {self.average_length}
Избыточность: {self.redundancy}
Неравенство Крафта {"строгое - сжатие оптимальное" if self.components_of_Kraft == 1 else "не строгое - сжатие не оптимальное"} ({self.components_of_Kraft})'''

    # Перевод числа с плавающей точкой в двоичную систему счисления.
    def decimal_to_binary_float(self, number, dl):
        """
        Преобразует десятичное число в двоичное с фиксированной длиной.
        number: float — исходное десятичное число.
        dl: int — требуемая длина двоичного представления.
        """
        result = ''
        for _ in range(dl):
            number *= 2
            result += str(number)[0]  # Добавляем первую цифру от числа.
            if number >= 1:
                number -= 1  # Если число больше или равно 1, отнимаем 1.
        return result

    # Алгоритм для кодирования последовательности.
    def encode(self, sequence: str):
        """
        Кодирует последовательность символов.
        sequence: str — строка, которую нужно закодировать.
        """
        self.result = ''
        for i in sequence:
            if i not in self.codes_for_symbols.keys():
                # Если символ отсутствует в алфавите, выбрасываем исключение.
                raise Exception(f'Один или несколько введённых символов отсутствует в предопределённом алфавите')
            for j in self.codes_for_symbols:
                if str(i) == str(j):
                    # Добавляем соответствующий код символа в результат.
                    self.result += self.codes_for_symbols[i]
        return self.result

    # Алгоритм для декодирования последовательности.
    def decode(self, sequence: str):
        """
        Декодирует двоичную последовательность в символы.
        sequence: str — двоичная строка, которую нужно декодировать.
        """
        self.result = ''
        # Находим минимальную и максимальную длины кодов.
        minimum_of_length = len(min(self.codes_for_symbols.values(), key=len))
        maximum_of_length = len(max(self.codes_for_symbols.values(), key=len))

        limit = len(sequence)  # Ограничение по длине последовательности.

        while sequence and limit:
            # Пробегаем от минимальной длины до максимальной.
            for i in range(minimum_of_length, maximum_of_length + 1):
                flag = True
                current = sequence[:i]  # Текущий подстрок из последовательности.
                for key, value in self.codes_for_symbols.items():
                    if str(current) == str(value):
                        # Если найден соответствующий код, добавляем символ в результат.
                        self.result += key
                        sequence = sequence[i:]  # Убираем закодированную часть из последовательности.
                        flag = False
                        break
                if not flag:
                    break
            limit -= 1

        # Если limit дошёл до 0, но последовательность не декодирована, выбрасываем исключение.
        if limit == 0:
            raise Exception(
                f'Последовательность не может быть декодирована, так как в ней присутствуют коды, неупомянутые в таблице кодов')
        return self.result


if __name__ == "__main__":
    # Пример вероятностей для символов.
    probs = {'+': '0.0', '-': '0.4', '*': '0.2', '/': '0.2', '=': '0.2'}

    # Пример последовательностей для кодирования и декодирования.
    seq = '++--**//=='
    seq1 = '0001000101000100100010001011101111101110'

    # Создаем объект кодировщика.
    g_m = GilbertMooreEncoder(probs=probs)

    # Основная программа.
    end = 1
    while end == 1:
        choice = int(input('''Выбери действие
    1 - Кодирование последовательности
    2 - Декодирование последовательности\n'''))

        if choice == 1:
            # Кодирование.
            g_m.encode(seq)
            print(str(g_m))
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))

        elif choice == 2:
            # Декодирование.
            g_m.decode(seq1)
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))

        else:
            print('Действие не выбрано :(')
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))
