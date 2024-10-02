import math
from fractions import Fraction

class Gilber_Murr:


    def __init__(self):
        pass
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
    def coding(self):
        with open('in1.txt', encoding='utf-8') as input_file1, open('in2.txt', encoding='utf-8') as input_file2:
            p = [i.strip().split() for i in input_file1.readlines()]
            stroka = input_file2.read().strip()
            mas_coding = {}
            q, sigma, l, summa_lenghts, entropia, Kraft = 0, 0, 0, 0, 0, 0

            for i in range(len(p)):
                entropia -= float(Fraction(p[i][1])) * math.log(float(Fraction(p[i][1])), 2)
                sigma = q + float(Fraction(p[i][1])) / 2
                q += float(Fraction(p[i][1]))
                l = int((-math.log(float(Fraction(p[i][1])) / 2, 2)) + 0.999999)
                summa_lenghts += l
                duble_number = decimal_to_binary_float(sigma, l)
                mas_coding[p[i][0]] = duble_number
                Kraft += 2 ** (-l)

            middle_lenght = summa_lenghts / len(p)
            redundancy = middle_lenght - entropia
            for key, value in mas_coding.items():
                print(f'Символ: \'{key}\' кодируется \'{value}\'')
            print(f'''Средняя длина: {middle_lenght}
    Избыточность: {redundancy}
    Крафт: {Kraft}''')
            with open('in3.txt', 'w', encoding='utf-8') as output_file:
                res = ''
                for i in stroka:
                    for j in mas_coding:
                        if str(i) == str(j):
                            res += mas_coding[i]
                print(res, file=output_file)
                print('Результат кодирования выведен в файл')


    # Алгоритм для декодирования последовательности
    def decoding(self):
        with open('in1.txt', encoding='utf-8') as input_file1, open('in3.txt', encoding='utf-8') as input_file2:
            p = [i.strip().split() for i in input_file1.readlines()]
            stroka = input_file2.read().strip()
            mas_coding = {}
            q, sigma, l, summa_lenghts, entropia, Kraft = 0, 0, 0, 0, 0, 0

            for i in range(len(p)):
                entropia -= float(Fraction(p[i][1])) * math.log(float(Fraction(p[i][1])), 2)
                sigma = q + float(Fraction(p[i][1])) / 2
                q += float(Fraction(p[i][1]))
                l = int((-math.log(float(Fraction(p[i][1])) / 2, 2)) + 0.999999)
                summa_lenghts += l
                duble_number = decimal_to_binary_float(sigma, l)
                mas_coding[p[i][0]] = duble_number
                Kraft += 2 ** (-l)

            middle_lenght = summa_lenghts / len(p)
            redundancy = middle_lenght - entropia
            for key, value in mas_coding.items():
                print(f'Символ: \'{key}\' кодируется \'{value}\'')
            print(f'''Средняя длина: {middle_lenght}
    Избыточность: {redundancy}
    Крафт: {Kraft}''')
            with open('in3.txt', 'w', encoding='utf-8') as output_file:
                res = ''
                a = len(min(mas_coding.values(), key=len))
                b = len(max(mas_coding.values(), key=len))
                while stroka:
                    for i in range(a, b + 1):
                        flag = True
                        current = stroka[:i]
                        for key, value in mas_coding.items():
                            if str(current) == str(value):
                                res += key
                                stroka = stroka[i:]
                                flag = False
                                break
                        if not flag:
                            break
                print(res, file=output_file)
                print('Результат декодирования выведен в файл')

if __name__ == "__main__":
    g_m = Gilber_Murr
    # Основная программа
    end = 1
    while end == 1:
        choice = int(input('''Выбери действие
    1 - Кодирование последовательности
    2 - Декодирование последовательности\n'''))
        if choice == 1:
            # with open('in1.txt', 'w', encoding='utf-8') as in1, open('in2.txt', 'w', encoding='utf-8') as in2:
            #     symbol1 = print(f'+ {float(Fraction(input('Введите вероятность для символа \'+\' ')))}', file=in1)
            #     symbol2 = print(f'- {float(Fraction(input('Введите вероятность для символа \'-\' ')))}', file=in1)
            #     symbol3 = print(f'* {float(Fraction(input('Введите вероятность для символа \'*\' ')))}', file=in1)
            #     symbol4 = print(f'/ {float(Fraction(input('Введите вероятность для символа \'/\' ')))}', file=in1)
            #     symbol5 = print(f'= {float(Fraction(input('Введите вероятность для символа \'=\' ')))}', file=in1)
            #     posled = print(f'{input('Введите строку для кодирования(декодирования)\n')}', file=in2)
            g_m.coding()
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))

        elif choice == 2:
            # with open('in1.txt', 'w', encoding='utf-8') as in1, open('in2.txt', 'w', encoding='utf-8') as in2:
            #     symbol1 = print(f'+ {float(Fraction(input('Введите вероятность для символа \'+\' ')))}', file=in1)
            #     symbol2 = print(f'- {float(Fraction(input('Введите вероятность для символа \'-\' ')))}', file=in1)
            #     symbol3 = print(f'* {float(Fraction(input('Введите вероятность для символа \'*\' ')))}', file=in1)
            #     symbol4 = print(f'/ {float(Fraction(input('Введите вероятность для символа \'/\' ')))}', file=in1)
            #     symbol5 = print(f'= {float(Fraction(input('Введите вероятность для символа \'=\' ')))}', file=in1)
            #     posled = print(f'{input('Введите строку для кодирования(декодирования)\n')}', file=in2)
            g_m.decoding()
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))

        else:
            print('Действие не выбрано :(')
            end = int(input('''Выбери действие
    1 - Выбрать следующее действие
    Другое - Остановить программу\n'''))