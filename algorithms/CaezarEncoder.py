class CaezarEncoder:
    def __init__(self, alphabet: str):
        self.alphabet = alphabet
        self.N = len(alphabet)

    def __repr__(self):
        return f'CaezarEncoder({self.alphabet})'

    def __str__(self):
        return

    def validation(self, shift):
        if shift <= 0:
            raise Exception("Сдвиг не может быть меньше 0")
        elif shift > self.N:
            raise Exception("Сдвиг не может быть больше 0")
        return

    def encoder(self, seq, shift):
        self.validation(shift)
        res = ''
        for char in seq:
            if char in self.alphabet:
                res += self.alphabet[(self.alphabet.index(char) + shift) % self.N]
            else:
                raise Exception("Какой(-ие)-то символ(-ы) отсутствуют в алфавите")
        return res

    def decoder(self, seq, shift):
        self.validation(shift)
        res = ''
        for char in seq:
            if char in self.alphabet:
                res += self.alphabet[(self.alphabet.index(char) - shift + self.N) % self.N]
            else:
                raise Exception("Какой(-ие)-то символ(-ы) отсутствуют в алфавите")
        return res



if __name__ == "__main__":
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    sequence = input('Введите последовательность: ')
    shift = int(input("Введите сдвиг: "))
    caezar = CaezarEncoder(alphabet)
    print("Результат кодировки: ", caezar.encoder(sequence, shift))
    sequence_d = input('Введите последовательность: ')
    print("Результат декодировки: ", caezar.decoder(sequence_d, shift))
