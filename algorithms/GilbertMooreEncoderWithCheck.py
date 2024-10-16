import math
from fractions import Fraction


class GilbertMooreEncoderWithCheck:

    def __init__(self, probs: dict):
        """
        Конструктор класса. Принимает словарь, в котором ключи — это символы, а значения — их вероятности (в виде строк).
        """
        self.probs = probs
        # Проверяем, что сумма вероятностей равна 1. Если нет, выбрасывается исключение.
        if sum(map(lambda x: float(Fraction(x)), probs.values())) != 1:
            raise Exception("Сумма вероятностей не равна 1")
        for i in range(len(self.probs.values()) - 1):
            if list(self.probs.values())[i] != list(self.probs.values())[i+1]:
                raise Exception("Алфавит не равномерный")
        self.probs = {key:value for key, value in probs.items() if float(Fraction(value)) != 0.0}

        self.codes_for_symbols = {}
        self.codes_for_symbols_old = {}  # Словарь для хранения кодов для каждого символа.
        q, sigma, length, sum_of_lengths, entropy = 0, 0, 0, 0, 0
        self.errors = []

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
            self.codes_for_symbols_old[i] = number_in_binary
        for key,value in self.codes_for_symbols.items():
            if sum(list(map(int, value))) % 2 == 0:
                self.codes_for_symbols[key] += '0'
            else:
                self.codes_for_symbols[key] += '1'

        self.distance = []
        for i in range(len(self.codes_for_symbols)):
            self.distance.append([])
            for j in range(len(self.codes_for_symbols)):
                self.distance[i].append(1000)

        for i in range(len(self.codes_for_symbols)):
            for j in range(i,len(self.codes_for_symbols)):
                if i != j:
                    self.distance[i][j] = sum(1 for c1, c2 in zip(list(self.codes_for_symbols.values())[i], list(self.codes_for_symbols.values())[j]) if c1 != c2)
                    self.distance[j][i] = self.distance[i][j]

    def __repr__(self):
        """
        Метод для представления объекта.
        """
        return f'Gilber-Murr({self.probs, self.result})'

    def __str__(self):
        """
        Метод для форматированного вывода информации о кодировании.
        """
        n = len(list(self.codes_for_symbols.values())[0])
        k = len(list(self.codes_for_symbols_old.values())[0])
        d0 = min(min(row) for row in self.distance)
        sum_comb_hamming = sum([math.comb(n, i) for i in range(int((d0-1)/2)+1)])
        sum_comb_varsh = sum([math.comb(n-1, i) for i in range(d0-2+1)])

        return f'''Алгоритм Гилберта-Мура с проверочными битами
{'\n'.join([f'Символ: \'{key}\' кодируется \'{value}\'' for key, value in self.codes_for_symbols.items()])}
Расстояния Хэмминга:
{'\n'.join(['\t'.join([f'd{i+1}_{j+1} = {self.distance[i][j]}' for j in range(i+1, len(self.codes_for_symbols))]) for i in range(len(self.codes_for_symbols)-1)])}
Кратсность обнаружения: q_обн <= {int(d0/2)}
Кратсность исправления: q_исп <= {int((d0-1)/2)}
Наименьшее расстояние Хэмминга: d0 = {d0}
Граница Хэмминга: r = n - k = {n - k} >= log2({sum_comb_hamming}) = {math.log2(sum_comb_hamming)} {' Не выполняется' if (math.log2(sum_comb_hamming) > (n - k)) else " Выполняется"}
Граница Плоткина: d0 = {min(min(row) for row in self.distance)} <= n * 2^(k-1) / (2^k – 1) = {n * pow(2,k-1) / (pow(2,k)-1)} {' Не выполняется' if (d0 > n * pow(2,k-1) / (pow(2,k)-1)) else " Выполняется"}
Граница Варшамова-Гильберта: 2^(n-k) = {pow(2, n-k)} > {sum_comb_varsh} {' Не выполняется' if (pow(2, n-k) <= sum_comb_varsh) else " Выполняется"}
'''


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
        current_index = 0
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
                        current_index += 1
                        break
                if not flag:
                    break
            if limit < len(sequence)/2:
                self.errors.append(f"word: {current_index+1}")
                self.result += ' '
                sequence = sequence[i:]
                limit = len(sequence)
            limit -= 1

        return self.result


if __name__ == "__main__":
    # Пример вероятностей для символов.
    probs = {'+': '0.2', '-': '0.2', '*': '0.2', '/': '0.2', '=': '0.2'}

    # Пример последовательностей для кодирования и декодирования.
    seq = '++--**//=='
    seq1 = '00011100110100101001100011000110111101111110111101'

    # Создаем объект кодировщика.
    g_m = GilbertMooreEncoderWithCheck(probs=probs)

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
            print(str(g_m))
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))

        else:
            print('Действие не выбрано :(')
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))
