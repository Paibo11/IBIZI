import random
import math
from collections import defaultdict
import time


class PlayfairCracker:
    def __init__(self):
        self.trigram_log_prob = self.load_real_trigram_frequencies()
        self.alphabet = 'abcdefghiklmnopqrstuvwxyz'  # без 'j'
        self.square_size = 5

    def load_real_trigram_frequencies(self):
        # Реальные частоты триграмм английского языка (топ-100)
        trigrams = {
            'the': 1.81, 'and': 0.73, 'ing': 0.72, 'ent': 0.42, 'ion': 0.42,
            'her': 0.36, 'for': 0.34, 'tha': 0.33, 'nth': 0.33, 'int': 0.32,
            'ere': 0.31, 'tio': 0.31, 'ter': 0.30, 'est': 0.28, 'ers': 0.28,
            'ati': 0.26, 'hat': 0.26, 'ate': 0.25, 'all': 0.25, 'eth': 0.24,
            'hes': 0.24, 'ver': 0.24, 'his': 0.24, 'oft': 0.22, 'ith': 0.22,
            'fth': 0.22, 'sth': 0.21, 'oth': 0.21, 'res': 0.21, 'ont': 0.20,
            'dth': 0.19, 'are': 0.19, 'rea': 0.19, 'ear': 0.19, 'was': 0.19,
            'sin': 0.18, 'sto': 0.18, 'tth': 0.18, 'sta': 0.18, 'thi': 0.17,
            'tin': 0.17, 'ted': 0.17, 'ngt': 0.16, 'ong': 0.16, 'tot': 0.16,
            'ese': 0.16, 'our': 0.16, 'red': 0.16, 'rom': 0.15, 'eve': 0.15,
            'din': 0.15, 'ess': 0.15, 'not': 0.15, 'hem': 0.15, 'edt': 0.15,
            'hin': 0.14, 'san': 0.14, 'nce': 0.14, 'ead': 0.14, 'whe': 0.14,
            'out': 0.14, 'era': 0.14, 'ead': 0.14, 'hey': 0.13, 'men': 0.13,
            'ela': 0.13, 'som': 0.13, 'lit': 0.13, 'ell': 0.13, 'she': 0.13,
            'ave': 0.13, 'han': 0.13, 'ndh': 0.13, 'bea': 0.13, 'ind': 0.13,
            'oug': 0.13, 'pro': 0.12, 'thr': 0.12, 'per': 0.12, 'eed': 0.12,
            'tic': 0.12, 'whi': 0.12, 'rat': 0.12, 'ate': 0.12, 'str': 0.12,
            'uch': 0.11, 'nde': 0.11, 'ass': 0.11, 'pri': 0.11, 'hel': 0.11,
            'rou': 0.11, 'nal': 0.11, 'ans': 0.11, 'com': 0.11, 'eac': 0.11,
            'con': 0.11, 'ter': 0.11, 'eco': 0.10, 'cou': 0.10, 'wit': 0.10
        }

        # Преобразование в логарифмическую шкалу
        total = sum(trigrams.values())
        log_trigrams = {}
        for trigram in trigrams:
            probability = trigrams[trigram] / total
            log_trigrams[trigram] = math.log(probability)

        # Дефолтное значение для неизвестных триграмм
        default_log_prob = math.log(1e-10)
        return defaultdict(lambda: default_log_prob, log_trigrams)

    def generate_random_key(self):
        # Генерация случайного ключа
        letters = list(self.alphabet)
        random.shuffle(letters)
        return ''.join(letters)

    def create_playfair_square(self, key):
        # Оптимизированное создание квадрата
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
        # Оптимизированная расшифровка
        plaintext = []
        ciphertext = ciphertext.lower().replace('j', 'i')
        pos_cache = {square[r][c]: (r, c)
                     for r in range(self.square_size)
                     for c in range(self.square_size)}

        for i in range(0, len(ciphertext) - 1, 2):
            a, b = ciphertext[i], ciphertext[i + 1]
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

        return ''.join(plaintext)

    def score_text(self, text):
        # Быстрая оценка текста
        score = 0
        text = text.lower()
        for i in range(len(text) - 2):
            score += self.trigram_log_prob[text[i:i + 3]]
        return score / (len(text) - 2) if len(text) > 2 else -100

    def mutate_key(self, key):
        # Улучшенные мутации
        key = list(key)
        mutation_type = random.choice(['swap', 'swap_row', 'swap_col', 'reverse_row', 'reverse_col'])

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

        return ''.join(key)

    def simulated_annealing(self, ciphertext, iterations=30000, initial_temp=15.0, cooling_rate=0.9997):
        print("\nStarting optimized Playfair cracker...")

        # Начальный случайный ключ
        current_key = self.generate_random_key()
        current_square = self.create_playfair_square(current_key)
        current_plain = self.decrypt(ciphertext, current_square)
        current_score = self.score_text(current_plain)

        best_key = current_key
        best_score = current_score
        best_plain = current_plain

        temperature = initial_temp
        start_time = time.time()
        last_improvement = 0

        for i in range(iterations):
            # Генерация нового ключа
            new_key = self.mutate_key(current_key)
            new_square = self.create_playfair_square(new_key)
            new_plain = self.decrypt(ciphertext, new_square)
            new_score = self.score_text(new_plain)

            # Принятие решения
            if new_score > current_score or random.random() < math.exp((new_score - current_score) / temperature):
                current_key, current_score, current_plain = new_key, new_score, new_plain

                if new_score > best_score:
                    best_key, best_score, best_plain = new_key, new_score, new_plain
                    last_improvement = i
                    elapsed = time.time() - start_time
                    print(f"\nIter {i}: Score={best_score:.4f} Time={elapsed:.1f}s")
                    print(f"Key: {best_key}")
                    print(f"Text: {best_plain[:100]}...")

            # Охлаждение
            temperature *= cooling_rate

            # Ранняя остановка если нет улучшений
            if i - last_improvement > 5000 and i > 10000:
                print("\nEarly stopping - no improvement for 5000 iterations")
                break

            # Периодический вывод прогресса
            if i % 2000 == 0:
                elapsed = time.time() - start_time
                print(f"Progress: {i}/{iterations} ({i / iterations * 100:.1f}%)")
                print(f"Current score: {current_score:.4f}, Best: {best_score:.4f}")
                print(f"Temp: {temperature:.2f}, Time: {elapsed:.1f}s")

        print("\nCracking completed!")
        return best_key, best_plain, best_score


def load_ciphertext(filename):
    with open(filename, 'r') as f:
        text = f.read()
    return ''.join([c.lower() for c in text if c.isalpha()]).replace('j', 'i')


if __name__ == "__main__":
    cracker = PlayfairCracker()

    # Загрузка зашифрованного текста
    ciphertext = load_ciphertext('LT_encrypted.txt')
    print(f"Loaded ciphertext with {len(ciphertext)} characters")

    # Запуск алгоритма
    best_key, best_plain, best_score = cracker.simulated_annealing(
        ciphertext,
        iterations=30000,
        initial_temp=15.0,
        cooling_rate=0.9997
    )

    print("\nFinal results:")
    print(f"Best key: {best_key}")
    print(f"Decrypted text start: {best_plain[:200]}...")
    print(f"Score: {best_score:.4f}")

    # Сохранение результатов
    with open('playfair_decrypted.txt', 'w') as f:
        f.write(f"Key: {best_key}\n\n")
        f.write(best_plain)

    print("Results saved to 'playfair_decrypted.txt'")