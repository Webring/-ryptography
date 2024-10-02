import math
from fractions import Fraction


class GilbertMooreEncoder:

    def __init__(self, probs: dict):
        self.probs = probs
        self.codes_for_symbols = {}
        q, sigma, length, sum_of_lengths, entropy, self.components_of_Kraft = 0, 0, 0, 0, 0, 0
        for i in probs.keys():
            entropy -= float(Fraction(probs[i])) * math.log(float(Fraction(probs[i])), 2)
            sigma = q + float(Fraction(probs[i])) / 2
            q += float(Fraction(probs[i]))
            length = int((-math.log(float(Fraction(probs[i])) / 2, 2)) + 0.999999)
            sum_of_lengths += length
            number_in_binary = self.decimal_to_binary_float(sigma, length)
            self.codes_for_symbols[i] = number_in_binary
            self.components_of_Kraft += 2 ** (-length)
        self.average_length = sum_of_lengths / len(probs)
        self.redundancy = self.average_length - entropy
    def __repr__(self):
        return f'Gilber-Murr({self.probs, self.result})'
    def __str__(self):
        return f'''{'\n'.join([f'Символ: \'{key}\' кодируется \'{value}\'' for key,value in self.codes_for_symbols.items()])}
Средняя длина: {self.average_length}
Избыточность: {self.redundancy}
Неравенство Крафта {"строгое - сжатие оптимальное" if self.components_of_Kraft==1 else "не строгое - сжатие не оптимальное"} ({self.components_of_Kraft})'''

    # Перевод числа с плавающей точкой в двочиную систему счисления
    def decimal_to_binary_float(self, number, dl):
        result = ''

        for _ in range(dl):
            number *= 2
            result += str(number)[0]
            if number >= 1:
                number -= 1

        return result

    # Алгоритм для кодирования последовательности
    def encode(self, sequence: str):
        self.result = ''
        for i in sequence:
            for j in self.codes_for_symbols:
                if str(i) == str(j):
                    self.result += self.codes_for_symbols[i]

        return self.result

    # Алгоритм для декодирования последовательности
    def decode(self, sequence: str):
        self.result = ''
        a = len(min(self.codes_for_symbols.values(), key=len))
        b = len(max(self.codes_for_symbols.values(), key=len))
        while sequence:
            for i in range(a, b + 1):
                flag = True
                current = sequence[:i]
                for key, value in self.codes_for_symbols.items():
                    if str(current) == str(value):
                        self.result += key
                        sequence = sequence[i:]
                        flag = False
                        break
                if not flag:
                    break
        return self.result


if __name__ == "__main__":
    probs = {'+': '0.2', '-': '0.2', '*': '0.2', '/': '0.2', '=': '0.2'}
    seq = '++--**//=='
    seq1 = '0001000101000100100010001011101111101110'
    g_m = GilbertMooreEncoder(probs=probs)
    # Основная программа
    end = 1
    while end == 1:
        choice = int(input('''Выбери действие
    1 - Кодирование последовательности
    2 - Декодирование последовательности\n'''))
        if choice == 1:
            g_m.encode(seq)
            print(str(g_m))
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))

        elif choice == 2:
            g_m.decode(seq1)
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))

        else:
            print('Действие не выбрано :(')
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))
