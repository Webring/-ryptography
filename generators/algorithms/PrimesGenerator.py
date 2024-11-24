import random
import time
class PrimesGenerator:
    def __init__(self, start_bit, end_bit):
        self.start_bit = start_bit
        self.end_bit = end_bit
        self.res = []
        self.time_of_program = 0
        self.number = 0

    def __repr__(self):
        return f'PrimesGenerator(start_bit={self.start_bit},end_bit={self.end_bit})'

    def __str__(self):
        return f'Сгенерированное простое число: {self.number}\nВремя выполнения программы: {self.time_of_program: .7f}\nРешето Эратосфена: {self.res}'

    def validation(self):
        if self.end_bit < self.start_bit:
            raise Exception("Максимальное число бит должно быть больше или равно минимальному!")

    def prime_test(self, number):
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                return False
        return True

    def sieve_of_Eratosthenes(self, number):
        sieve = [i for i in range(2, number + 1)]
        for i in range(2, int(number ** 0.5) + 1):
            sieve = list(filter(lambda x: x % i != 0 or x == i, sieve))
        return sieve

    def prime_generate(self):
        n = random.randint(self.start_bit, self.end_bit)
        s = '1' + '0' * (n - 2) + '1'
        return int(s, 2)
    def generate(self):
        self.validation();
        start_time = time.perf_counter()
        self.number = self.prime_generate()
        while True:
            if self.prime_test(self.number):
                break
            else:
                self.number += 1
        self.res = self.sieve_of_Eratosthenes(self.number)
        end_time = time.perf_counter()
        self.time_of_program = end_time - start_time


if __name__ == "__main__":
    start = 1
    end = 10
    prime_gen = PrimesGenerator(start,end)
    prime_gen.generate()
    print(str(prime_gen))
    print(repr(prime_gen))