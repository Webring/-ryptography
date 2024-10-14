from GilbertMooreEncoderWithCheck import GilbertMooreEncoderWithCheck
import numpy as np
import math


class HammingCode:
    def __init__(self, probs: dict, hamming_matrix):
        # Создаем экземпляр GilbertMooreEncoder
        self.hamming_matrix = hamming_matrix
        self.encoder = GilbertMooreEncoderWithCheck(probs)
        self.G = self.generate_hamming_matrix()
        self.codes_for_symbols_GM = self.encoder.codes_for_symbols
        self.codes_hamming = {}
        for key,value in self.codes_for_symbols_GM.items():
            value_list = [int(digit) for digit in value]
            code_with_checkers = self.vector_matrix_mult(value_list, self.G)
            self.codes_hamming[key] = ''.join(str(num) for num in code_with_checkers)
        self.result = ''
        self.distance = []
        for i in range(len(self.codes_hamming)):
            self.distance.append([])
            for j in range(len(self.codes_hamming)):
                self.distance[i].append(1000)

        self.errors = []
        self.sindrome = 0
    def __repr__(self):
        """
        Метод для представления объекта.
        """
        return f'Hamming({self.hamming_matrix})'

    def __str__(self):
        """
        Метод для форматированного вывода информации о кодировании.
        """
        n = len(list(self.codes_hamming.values())[0])
        k = len(list(self.codes_for_symbols_GM.values())[0])
        d0 = min(min(row) for row in self.distance)
        sum_comb_hamming = sum([math.comb(n, i) for i in range(int((d0 - 1) / 2) + 1)])
        sum_comb_varsh = sum([math.comb(n - 1, i) for i in range(d0 - 2 + 1)])

        return f'''{'\n'.join([f'Символ: \'{key}\' кодируется \'{value}\'' for key, value in self.codes_hamming.items()])}
Расстояния Хэмминга:
{'\n'.join(['\t'.join([f'd{i + 1}_{j + 1} = {self.distance[i][j]}' for j in range(i + 1, len(self.codes_hamming))]) for i in range(len(self.codes_hamming) - 1)])}
Кратсность обнаружения: q_обн <= {math.ceil(d0 / 2)}
Кратсность исправления: q_исп <= {int((d0 - 1) / 2)}
Наименьшее расстояние Хэмминга: d0 = {d0}
Граница Хэмминга: r = n - k = {n - k} >= log2({sum_comb_hamming}) = {math.log2(sum_comb_hamming)} {' Не выполняется' if (math.log2(sum_comb_hamming) > (n - k)) else " Выполняется"}
Граница Плоткина: d0 = {min(min(row) for row in self.distance)} <= n * 2^(k-1) / (2^k – 1) = {n * pow(2, k - 1) / (pow(2, k) - 1)} {' Не выполняется' if (d0 > n * pow(2, k - 1) / (pow(2, k) - 1)) else " Выполняется"}
Граница Варшамова-Гильберта: 2^(n-k) = {pow(2, n - k)} > {sum_comb_varsh} {' Не выполняется' if (pow(2, n - k) <= sum_comb_varsh) else " Выполняется"}
'''


    def generate_hamming_matrix(self):
        """
        Генерирует проверочную матрицу H и генерирующую матрицу G.
        """
        # Генерирующая матрица G
        G = np.zeros((4, 7), dtype=int)

        # Заполнение генерирующей матрицы
        G[:, :4] = np.eye(4, dtype=int)  # Единичная матрица 4x4
        H_transposed = np.transpose(self.hamming_matrix)
        G[:, 4:] = np.array(H_transposed[:4])  # Проверочные биты (из H)

        return G

    def even_odd(self, num):
        return num % 2

    def vector_matrix_mult(self, v, m):
        """
        Умножает вектор на матрицу и возвращает результат.
        """
        result = np.dot(v, m)
        return list(map(self.even_odd, result))

    def convert(self, v, position):
        """
        Исправляет бит в векторе на указанной позиции.
        """
        if v[position] == 1:
            v[position] = 0
        else:
            v[position] = 1
        print(f"Был исправлен бит на {position + 1} позиции")
        return v

    def check_and_correct(self, v):
        """
        Проверяет и исправляет ошибки в кодовом слове v.
        """
        hamming_matrix_transposed = np.transpose(self.hamming_matrix)
        s = self.vector_matrix_mult(v, hamming_matrix_transposed)


        for i in range(7):
            if np.array_equal(s, hamming_matrix_transposed[i]):
                if i + 1 == 2:
                    self.sindrome = 2
                    print(f"Ошибка во 2 бите")
                    v = self.convert(v, i)
                    break
                self.sindrome = i+1
                print(f"Ошибка в {i + 1} бите")
                v = self.convert(v, i)
                break
        return v

    def encode(self, sequence: str):
        """
                Кодирует последовательность символов.
                sequence: str — строка, которую нужно закодировать.
                """
        self.result = ''
        for i in sequence:
            if i not in self.codes_hamming.keys():
                # Если символ отсутствует в алфавите, выбрасываем исключение.
                raise Exception(f'Один или несколько введённых символов отсутствует в предопределённом алфавите')
            for j in self.codes_hamming:
                if str(i) == str(j):
                    # Добавляем соответствующий код символа в результат.
                    self.result += self.codes_hamming[i]

        codes_list = list(self.codes_hamming.values())
        for i in range(len(self.codes_hamming)):
            for j in range(i, len(self.codes_hamming)):
                if i != j:
                    self.distance[i][j] = sum(1 for c1, c2 in zip(codes_list[i], codes_list[j]) if c1 != c2)
                    self.distance[j][i] = self.distance[i][j]

        return self.result

    def decode(self, sequence: str):
        """
        Декодирует двоичную последовательность в символы.
        sequence: str — двоичная строка, которую нужно декодировать.
        """
        self.result = ''
        # Находим минимальную и максимальную длины кодов.
        minimum_of_length = len(min(self.codes_hamming.values(), key=len))
        maximum_of_length = len(max(self.codes_hamming.values(), key=len))

        limit = len(sequence)  # Ограничение по длине последовательности.
        current_index = 0
        current = ''
        while sequence and limit:
            # Пробегаем от минимальной длины до максимальной.
            for i in range(minimum_of_length, maximum_of_length + 1):
                flag = True
                current = sequence[:i]  # Текущий подстрок из последовательности.
                for key, value in self.codes_hamming.items():
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
                current_list = [int(digit) for digit in current]
                correct_vector = self.check_and_correct(current_list)
                self.errors.append(f"word: {current_index+1}, bit: {self.sindrome}")
                self.result += ''.join(str(num) for num in correct_vector)
                sequence = sequence[i:]
                limit = len(sequence)
            limit -= 1

        return self.result

if __name__ == "__main__":
    H = [
        [1, 1, 0, 1, 1, 0, 0],
        [1, 1, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 1]
    ]
    probs = {'+': '0.2', '-': '0.2', '*': '0.2', '/': '0.2', '=': '0.2'}

    hamming_code = HammingCode(hamming_matrix=H, probs=probs)

    hamming_code.encode('+-/')
    print(hamming_code.result)
    print(hamming_code.check_and_correct([0,0,0,1,1,0,1]))

    hamming_code.decode('000110101011111011000')
    print(hamming_code.errors)
    # Кодовое слово
    # code = [0, 0, 1, 1]
    #
    # # Генерация кода
    # v = hamming_code.vector_matrix_mult(code, hamming_code.G)
    # print(f"Закодированное слово: {v}")
    #
    # # Эмулируем ошибку
    # v[3] = 0
    # print(f"Слово с ошибкой: {v}")
    #
    # # Проверка и исправление
    # corrected_vector = hamming_code.check_and_correct(v)
    # print(f"Исправленное слово: {corrected_vector}")

    print(str(hamming_code))