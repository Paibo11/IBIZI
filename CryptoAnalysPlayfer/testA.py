import random
import math
from collections import Counter, defaultdict
import time
import matplotlib.pyplot as plt


class PlayfairCracker:
    def __init__(self):
        self.alphabet = 'abcdefghiklmnopqrstuvwxyz'  # без 'j'
        self.square_size = 5
        self.trigram_freq = self.load_trigram_frequencies()
        self.bigram_freq = self.load_bigram_frequencies()
        self.letter_freq = self.load_letter_frequencies()

    def load_trigram_frequencies(self):
        # Топ-50 триграмм английского языка
        return {
            'the': 0.0181, 'and': 0.0073, 'ing': 0.0072, 'ion': 0.0042, 'ent': 0.0042,
            'her': 0.0036, 'for': 0.0034, 'tha': 0.0033, 'nth': 0.0033, 'int': 0.0032,
            'ere': 0.0031, 'tio': 0.0031, 'ter': 0.0030, 'est': 0.0028, 'ers': 0.0028,
            'ati': 0.0026, 'hat': 0.0026, 'ate': 0.0025, 'all': 0.0025, 'eth': 0.0024,
            'his': 0.0024, 'ver': 0.0024, 'you': 0.0022, 'ith': 0.0022, 'ght': 0.0022,
            'oul': 0.0021, 'nde': 0.0020, 'are': 0.0020, 'ess': 0.0020, 'not': 0.0019,
            'hin': 0.0019, 'edt': 0.0019, 'men': 0.0019, 'som': 0.0018, 'iti': 0.0018,
            'one': 0.0018, 'out': 0.0018, 'rea': 0.0018, 'our': 0.0018, 'ear': 0.0017,
            'whi': 0.0017, 'tth': 0.0017, 'dth': 0.0017, 'heh': 0.0017, 'ewa': 0.0016,
            'sto': 0.0016, 'ast': 0.0016, 'ill': 0.0016, 'com': 0.0016, 'per': 0.0016
        }

    def load_bigram_frequencies(self):
        # Топ-50 биграмм английского языка
        return {
            'th': 0.0388, 'he': 0.0368, 'in': 0.0228, 'er': 0.0218, 'an': 0.0214,
            're': 0.0174, 'nd': 0.0157, 'at': 0.0149, 'on': 0.0142, 'nt': 0.0137,
            'ha': 0.0133, 'es': 0.0128, 'st': 0.0126, 'en': 0.0126, 'ed': 0.0125,
            'to': 0.0118, 'it': 0.0115, 'ou': 0.0115, 'ea': 0.0114, 'hi': 0.0109,
            'is': 0.0102, 'or': 0.0098, 'ti': 0.0097, 'as': 0.0096, 'te': 0.0095,
            'et': 0.0093, 'ng': 0.0089, 'of': 0.0088, 'al': 0.0088, 'de': 0.0086,
            'se': 0.0084, 'le': 0.0083, 'sa': 0.0082, 'si': 0.0079, 'ar': 0.0078,
            've': 0.0075, 'ra': 0.0072, 'ld': 0.0071, 'ur': 0.0070, 'me': 0.0069,
            'ne': 0.0068, 'wa': 0.0067, 'll': 0.0066, 'tt': 0.0065, 'ff': 0.0064,
            'ss': 0.0063, 'ee': 0.0063, 'oo': 0.0062, 'ca': 0.0061, 'el': 0.0061
        }

    def load_letter_frequencies(self):
        # Частоты букв английского языка
        return {
            'e': 0.1270, 't': 0.0906, 'a': 0.0817, 'o': 0.0751, 'i': 0.0697,
            'n': 0.0675, 's': 0.0633, 'h': 0.0609, 'r': 0.0599, 'd': 0.0425,
            'l': 0.0403, 'c': 0.0278, 'u': 0.0276, 'm': 0.0241, 'w': 0.0236,
            'f': 0.0223, 'g': 0.0202, 'y': 0.0197, 'p': 0.0193, 'b': 0.0149,
            'v': 0.0098, 'k': 0.0077, 'x': 0.0015, 'j': 0.0015, 'q': 0.0010,
            'z': 0.0007
        }

    def generate_random_key(self):
        # Генерация случайного ключа
        letters = list(self.alphabet)
        random.shuffle(letters)
        return ''.join(letters)

    def create_playfair_square(self, key):
        # Создание квадрата Плейфера
        square = []
        used = set()

        for char in key.lower().replace('j', 'i'):
            if char not in used and char in self.alphabet:
                used.add(char)
                square.append(char)

        for char in self.alphabet:
            if char not in used:
                square.append(char)

        return [square[i * self.square_size:(i + 1) * self.square_size]
                for i in range(self.square_size)]

    def decrypt(self, ciphertext, square):
        # Расшифровка текста
        plaintext = []
        ciphertext = ciphertext.lower().replace('j', 'i')
        pos_cache = {square[r][c]: (r, c)
                     for r in range(self.square_size)
                     for c in range(self.square_size)}

        for i in range(0, len(ciphertext) - 1, 2):
            a, b = ciphertext[i], ciphertext[i + 1]

            try:
                row_a, col_a = pos_cache[a]
                row_b, col_b = pos_cache[b]

                if row_a == row_b:
                    plaintext.append(square[row_a][(col_a - 1) % 5])
                    plaintext.append(square[row_b][(col_b - 1) % 5])
                elif col_a == col_b:
                    plaintext.append(square[(row_a - 1) % 5][col_a])
                    plaintext.append(square[(row_b - 1) % 5][col_b])
                else:
                    plaintext.append(square[row_a][col_b])
                    plaintext.append(square[row_b][col_a])
            except KeyError:
                continue

        return ''.join(plaintext)

    def fitness(self, text):
        # Комплексная оценка текста
        score = 0
        text = text.lower()
        length = len(text)

        # Оценка по триграммам
        trigram_score = 0
        for i in range(length - 2):
            trigram = text[i:i + 3]
            trigram_score += self.trigram_freq.get(trigram, -10)
        score += trigram_score * 2

        # Оценка по биграммам
        bigram_score = 0
        for i in range(length - 1):
            bigram = text[i:i + 2]
            bigram_score += self.bigram_freq.get(bigram, -5)
        score += bigram_score

        # Оценка по частотам букв
        letter_counts = Counter(text)
        for letter in letter_counts:
            expected = self.letter_freq.get(letter, 0.0001) * length
            actual = letter_counts[letter]
            score -= abs(expected - actual) * 0.1

        # Штраф за редкие сочетания
        rare_pairs = ['qq', 'zx', 'qk', 'zq', 'xj']
        for pair in rare_pairs:
            if pair in text:
                score -= 5

        return score / length if length > 10 else -100

    def mutate(self, key):
        # Различные типы мутаций
        key = list(key)
        mutation_type = random.choice([
            'swap', 'swap_row', 'swap_col',
            'reverse_row', 'reverse_col',
            'shuffle_row', 'shuffle_col'
        ])

        if mutation_type == 'swap':
            i, j = random.sample(range(25), 2)
            key[i], key[j] = key[j], key[i]
        elif mutation_type == 'swap_row':
            i, j = random.sample(range(5), 2)
            for k in range(5):
                key[i * 5 + k], key[j * 5 + k] = key[j * 5 + k], key[i * 5 + k]
        elif mutation_type == 'swap_col':
            i, j = random.sample(range(5), 2)
            for k in range(5):
                key[k * 5 + i], key[k * 5 + j] = key[k * 5 + j], key[k * 5 + i]
        elif mutation_type == 'reverse_row':
            row = random.randint(0, 4)
            key[row * 5:(row + 1) * 5] = reversed(key[row * 5:(row + 1) * 5])
        elif mutation_type == 'reverse_col':
            col = random.randint(0, 4)
            for row in range(2):
                key[row * 5 + col], key[(4 - row) * 5 + col] = key[(4 - row) * 5 + col], key[row * 5 + col]
        elif mutation_type == 'shuffle_row':
            row = random.randint(0, 4)
            row_letters = key[row * 5:(row + 1) * 5]
            random.shuffle(row_letters)
            key[row * 5:(row + 1) * 5] = row_letters
        elif mutation_type == 'shuffle_col':
            col = random.randint(0, 4)
            col_letters = [key[row * 5 + col] for row in range(5)]
            random.shuffle(col_letters)
            for row in range(5):
                key[row * 5 + col] = col_letters[row]

        return ''.join(key)

    def crossover(self, parent1, parent2):
        # Упорядоченный кроссовер
        child = [''] * 25
        start, end = sorted(random.sample(range(25), 2))
        child[start:end] = parent1[start:end]

        remaining = [c for c in parent2 if c not in child[start:end]]
        ptr = 0
        for i in range(25):
            if child[i] == '':
                child[i] = remaining[ptr]
                ptr += 1
        return ''.join(child)

    def genetic_algorithm(self, ciphertext, population_size=100, generations=500):
        # Инициализация популяции
        population = [self.generate_random_key() for _ in range(population_size)]
        best_score = -float('inf')
        best_key = None
        best_plain = None
        history = []

        for gen in range(generations):
            # Оценка приспособленности
            scored = []
            for key in population:
                square = self.create_playfair_square(key)
                plain = self.decrypt(ciphertext, square)
                score = self.fitness(plain)
                scored.append((score, key, plain))

            # Сортировка по приспособленности
            scored.sort(reverse=True, key=lambda x: x[0])

            # Отбор лучших
            elites = [key for (score, key, plain) in scored[:10]]
            new_population = elites.copy()

            # Размножение
            while len(new_population) < population_size:
                parent1, parent2 = random.choices(elites, k=2)
                child = self.crossover(parent1, parent2)
                if random.random() < 0.3:  # Вероятность мутации
                    child = self.mutate(child)
                new_population.append(child)

            population = new_population

            # Отслеживание лучшего результата
            current_best_score, current_best_key, current_best_plain = scored[0]
            if current_best_score > best_score:
                best_score = current_best_score
                best_key = current_best_key
                best_plain = current_best_plain
                history.append(best_score)

                print(f"\nGeneration {gen}: New best score = {best_score:.4f}")
                print(f"Key: {best_key}")
                print(f"Plaintext start: {best_plain[:100]}...")

            # Ранняя остановка если нет улучшений
            if gen > 50 and len(history) > 10 and abs(history[-1] - history[-10]) < 0.01:
                print("\nEarly stopping - convergence detected")
                break

        return best_key, best_plain, best_score

    def plot_history(self, history):
        plt.figure(figsize=(10, 5))
        plt.plot(history)
        plt.title("Fitness Score Improvement")
        plt.xlabel("Generation")
        plt.ylabel("Fitness Score")
        plt.grid(True)
        plt.show()


def load_ciphertext(filename):
    with open(filename, 'r') as f:
        text = f.read()
    return ''.join([c.lower() for c in text if c.isalpha()]).replace('j', 'i')


if __name__ == "__main__":
    cracker = PlayfairCracker()

    # Загрузка зашифрованного текста
    ciphertext = load_ciphertext('LT_encrypted.txt')
    print(f"Loaded ciphertext with {len(ciphertext)} characters")

    # Запуск генетического алгоритма
    start_time = time.time()
    best_key, best_plain, best_score = cracker.genetic_algorithm(
        ciphertext,
        population_size=100,
        generations=500
    )
    elapsed = time.time() - start_time

    print("\nFinal results:")
    print(f"Best key found: {best_key}")
    print(f"Decrypted text start: {best_plain[:200]}...")
    print(f"Fitness score: {best_score:.4f}")
    print(f"Time elapsed: {elapsed:.2f} seconds")

    # Сохранение результатов
    with open('playfair_decrypted.txt', 'w') as f:
        f.write(f"Key: {best_key}\n\n")
        f.write(best_plain)

    print("\nResults saved to 'playfair_decrypted.txt'")