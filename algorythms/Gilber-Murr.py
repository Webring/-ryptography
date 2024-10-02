import math
from fractions import Fraction

class Gilber_Murr:


    def __init__(self, probs: dict):
        self.probs = probs
        self.mas_coding = {}
        q, sigma, l, summa_lenghts, entropia, self.kraft = 0, 0, 0, 0, 0, 0
        for i in p.keys():
            entropia -= float(Fraction(p[i])) * math.log(float(Fraction(p[i])), 2)
            sigma = q + float(Fraction(p[i])) / 2
            q += float(Fraction(p[i]))
            l = int((-math.log(float(Fraction(p[i])) / 2, 2)) + 0.999999)
            summa_lenghts += l
            duble_number = self.decimal_to_binary_float(sigma, l)
            mas_coding[i] = duble_number
            self.kraft += 2 ** (-l)
        self.middle_lenght = summa_lenghts / len(p)
        redundancy = middle_lenght - entropia

    # Перевод числа с плавающей точкой в двочиную систему счисления
    def decimal_to_binary_float(self,number, dl):
        res = ''

        for _ in range(dl):
            number *= 2
            res += str(number)[0]
            if number >= 1:
                number -= 1

        return res

    # Алгоритм для кодирования последовательности
    def encoding(self, sequence: str):

        p = self.probs





        for key, value in mas_coding.items():
            print(f'Символ: \'{key}\' кодируется \'{value}\'')
        print(f'Средняя длина: {middle_lenght}\n'
               f'Избыточность: {redundancy}\n'
                f'Крафт: {Kraft}')
        res = ''
        for i in sequence:
            for j in mas_coding:
                if str(i) == str(j):
                    res += mas_coding[i]

        return res, mas_coding, middle_lenght, redundancy, Kraft


    # Алгоритм для декодирования последовательности
    def decoding(self,sequence: str):
        p = self.probs
        q, sigma, l, summa_lenghts, entropia, Kraft = 0, 0, 0, 0, 0, 0

        for i in p.keys():
            entropia -= float(Fraction(p[i])) * math.log(float(Fraction(p[i])), 2)
            sigma = q + float(Fraction(p[i])) / 2
            q += float(Fraction(p[i]))
            l = int((-math.log(float(Fraction(p[i])) / 2, 2)) + 0.999999)
            summa_lenghts += l
            duble_number = self.decimal_to_binary_float(sigma, l)
            mas_coding[i] = duble_number
            Kraft += 2 ** (-l)

        middle_lenght = summa_lenghts / len(p)
        redundancy = middle_lenght - entropia
        for key, value in mas_coding.items():
            print(f'Символ: \'{key}\' кодируется \'{value}\'')
        print(f'Средняя длина: {middle_lenght}\n Избыточность: {redundancy}\n Крафт: {Kraft}')
        res = ''
        a = len(min(mas_coding.values(), key=len))
        b = len(max(mas_coding.values(), key=len))
        while sequence:
            for i in range(a, b + 1):
                flag = True
                current = sequence[:i]
                for key, value in mas_coding.items():
                    if str(current) == str(value):
                        res += key
                        sequence = sequence[i:]
                        flag = False
                        break
                if not flag:
                    break
        return res, mas_coding, middle_lenght, redundancy, Kraft

if __name__ == "__main__":
    probs = {'+':'0.2','-':'0.2','*':'0.2','/':'0.2','=':'0.2'}
    seq = '++--**//=='
    seq1 = '0001000101000100100010001011101111101110'
    g_m = Gilber_Murr(probs=probs)
    # Основная программа
    end = 1
    while end == 1:
        choice = int(input('''Выбери действие
    1 - Кодирование последовательности
    2 - Декодирование последовательности\n'''))
        if choice == 1:
            # with open('in1.csv', 'w', encoding='utf-8') as in1, open('in2.txt', 'w', encoding='utf-8') as in2:
            #     symbol1 = print(f'+ {float(Fraction(input('Введите вероятность для символа \'+\' ')))}', file=in1)
            #     symbol2 = print(f'- {float(Fraction(input('Введите вероятность для символа \'-\' ')))}', file=in1)
            #     symbol3 = print(f'* {float(Fraction(input('Введите вероятность для символа \'*\' ')))}', file=in1)
            #     symbol4 = print(f'/ {float(Fraction(input('Введите вероятность для символа \'/\' ')))}', file=in1)
            #     symbol5 = print(f'= {float(Fraction(input('Введите вероятность для символа \'=\' ')))}', file=in1)
            #     posled = print(f'{input('Введите строку для кодирования(декодирования)\n')}', file=in2)
            g_m.encoding(seq)
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))

        elif choice == 2:
            # with open('in1.csv', 'w', encoding='utf-8') as in1, open('in2.txt', 'w', encoding='utf-8') as in2:
            #     symbol1 = print(f'+ {float(Fraction(input('Введите вероятность для символа \'+\' ')))}', file=in1)
            #     symbol2 = print(f'- {float(Fraction(input('Введите вероятность для символа \'-\' ')))}', file=in1)
            #     symbol3 = print(f'* {float(Fraction(input('Введите вероятность для символа \'*\' ')))}', file=in1)
            #     symbol4 = print(f'/ {float(Fraction(input('Введите вероятность для символа \'/\' ')))}', file=in1)
            #     symbol5 = print(f'= {float(Fraction(input('Введите вероятность для символа \'=\' ')))}', file=in1)
            #     posled = print(f'{input('Введите строку для кодирования(декодирования)\n')}', file=in2)
            g_m.decoding(seq1)
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))

        else:
            print('Действие не выбрано :(')
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))