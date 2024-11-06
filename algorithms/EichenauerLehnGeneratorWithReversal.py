from scipy.stats import chisquare
from collections import Counter


# Функция для нахождения обратного элемента по модулю
def reverse_to_mod(x, n):
    for i in range(1, n):
        if (x * i) % n == 1:
            return i
    return None


# Функция для генерации последовательности
def generate(x, a, c, n):
    if x == 0:
        return c
    else:
        result = (reverse_to_mod(x, n) * a + c) % n
    return result


# Функция для проверки входных данных
def validation(a, c, x, n):
    return 0 <= a < n and 0 <= c < n and 0 <= x < n

# Функция для подсчета периода
def period(array):
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


# Функция для проверки качества сгенерированной последовательности
def check_sequence_quality(sequence):
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
    # Применение критерия согласия Пирсона
    8
    chi2_stat, p_value = chisquare(observed_values, expected_values)
    alpha = 0.05  # уровень значимости
    if p_value < alpha:
        return 'Последовательность отклоняется от ожидаемого распределения (H0 отвергается).'
    else:
        return "Нет оснований отвергать нулевую гипотезу (H0): последовательность соответствует ожидаемому распределению."


# Функция для запуска генерации последовательности и вывода результатов
def run_generation():
    try:
        N = int(input("Введите N: "))
        a = int(input("Введите a: "))
        c = int(input("Введите c: "))
        x0 = int(input("Введите x0: "))
        mas = [x0]
        if validation(a, c, x0, N):
            for _ in range(N):
                mas.append(generate(mas[-1], a, c, N))
            seq_period = period(mas)
            check = check_sequence_quality(mas)
            output_text = (f'Последовательность значений: {mas}\n'
                           f'Период: {seq_period}\n'
                           f'Пирсон: {check}')
            print("Результаты", output_text)
        else:
            print("Ошибка", 'Введены некорректные данные')
    except ValueError:
        print("Ошибка", 'Пожалуйста, введите корректные целые числа')

if __name__ == "__main__":
    run_generation()