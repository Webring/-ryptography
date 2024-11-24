from scipy.stats import chisquare
from collections import Counter
import numpy as np


class EichenauerLehnGeneratorWithReversal:
    def __init__(self, N, a, c, x_0):
        self.N = N
        self.a = a
        self.c = c
        self.x_0 = x_0
        self.p_value = 0
        self.alpha = 0.05
        self.mas = []
        self.output_text = ''
        if not self.validation():
            raise Exception("Входные данные были заданы неверно")

    def __repr__(self):
        return f'EichenauerLehnGeneratorWithReversal(N = {self.N},a = {self.a},c = {self.c},x_0 = {self.x_0})'

    def __str__(self):
        return f'{self.output_text}\n {'Последовательность отклоняется от ожидаемого распределения (H0 отвергается).' if self.p_value < self.alpha
        else "Нет оснований отвергать нулевую гипотезу (H0): последовательность соответствует ожидаемому распределению."}'

    def validation(self):
        if int(np.log2(self.N)) != np.log2(self.N):
            raise Exception("'N' должна быть степенью двойки")
        if self.a % 2 == 0:
            raise Exception("Коэффициент 'a' должен быть нечётным")
        if self.c % 2 == 1:
            raise Exception("Коэффициент 'c' должен быть чётным")
        if self.x_0 % 2 == 0:
            raise Exception("Начальное значение 'x0' должно быть нечётным")
        return 0 <= self.a < self.N and 0 <= self.c < self.N and 0 <= self.x_0 < self.N

    def reverse_to_mod(self, x):
        for i in range(1, self.N):
            if (x * i) % self.N == 1:
                return i
        return None

    def generate(self, x):
        if x == 0:
            return self.c
        else:
            result = (self.reverse_to_mod(x) * self.a + self.c) % self.N
        return result

    def period(self, array):
        point = array[0]
        k = 0
        dl = 0
        for i in array:
            if i == point:
                dl += 1
            if dl == 2:
                break
            k += 1
        return k

    def check_sequence_quality(self, sequence):
        length = len(sequence)
        # Подсчет частоты значений
        observed_counts = Counter(sequence)
        # Ожидаемая частота
        expected_count = length / len(set(sequence))
        expected_counts = {value: expected_count for value in observed_counts.keys()}
        # Сбор значений и частот для теста Пирсона
        observed_values = []
        expected_values = []
        for value in sorted(expected_counts.keys()):
            observed_values.append(observed_counts.get(value, 0))
            expected_values.append(expected_counts[value])
        # Применение критерия Пирсона
        chi2_stat, self.p_value = chisquare(observed_values, expected_values)

    def run_generation(self):
        self.mas = [self.x_0]
        for _ in range(self.N):
            self.mas.append(self.generate(self.mas[-1]))
            seq_period = self.period(self.mas)
            self.check_sequence_quality(self.mas)
            self.output_text = (f'Последовательность значений: {self.mas}\n'
                                f'Период: {seq_period}\n'
                                f'Пирсон: ')


if __name__ == "__main__":
    N = int(input("Введите N: "))
    a = int(input("Введите a: "))
    c = int(input("Введите c: "))
    x0 = int(input("Введите x0: "))
    EL = EichenauerLehnGeneratorWithReversal(N, a, c, x0)
    EL.run_generation()
    print(str(EL))
