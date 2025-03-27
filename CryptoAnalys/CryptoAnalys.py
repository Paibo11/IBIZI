import re
from collections import Counter
import matplotlib
matplotlib.use('TkAgg')  # Устанавливаем бэкенд перед импортом pyplot
import matplotlib.pyplot as plt
import numpy as np
from itertools import product
from math import gcd
from functools import reduce

# Частотный анализ для русского языка (примерные частоты)
RUSSIAN_LETTER_FREQ = {
    'о': 0.1097, 'е': 0.0845, 'а': 0.0801, 'и': 0.0735, 'н': 0.0670,
    'т': 0.0626, 'с': 0.0547, 'р': 0.0473, 'в': 0.0454, 'л': 0.0440,
    'к': 0.0349, 'м': 0.0321, 'д': 0.0298, 'п': 0.0281, 'у': 0.0262,
    'я': 0.0201, 'ы': 0.0190, 'ь': 0.0174, 'г': 0.0170, 'з': 0.0165,
    'б': 0.0159, 'ч': 0.0144, 'й': 0.0121, 'х': 0.0097, 'ж': 0.0094,
    'ш': 0.0073, 'ю': 0.0064, 'ц': 0.0048, 'щ': 0.0036, 'э': 0.0032,
    'ф': 0.0026, 'ъ': 0.0004, 'ё': 0.0004
}

RUSSIAN_BIGRAM_FREQ = {
    'ст': 0.018, 'но': 0.016, 'то': 0.015, 'на': 0.014, 'ен': 0.013,
    'ов': 0.012, 'ни': 0.012, 'ра': 0.011, 'во': 0.011, 'ко': 0.011,
    'по': 0.010, 'ос': 0.010, 'ер': 0.010, 'пр': 0.010, 'не': 0.010,
    'ал': 0.009, 'ли': 0.009, 'ро': 0.009, 'ет': 0.009, 'ан': 0.009,
    'ло': 0.008, 'ор': 0.008, 'ес': 0.008, 'тв': 0.008, 'ре': 0.008,
    'та': 0.008, 'ел': 0.008, 'ин': 0.008, 'де': 0.008, 'на': 0.008,
    'ка': 0.007, 'от': 0.007, 'го': 0.007, 'до': 0.007, 'ит': 0.007,
    'мо': 0.007, 'ом': 0.007, 'за': 0.007, 'че': 0.007, 'те': 0.007,
    'ль': 0.007, 'ес': 0.007, 'об': 0.007, 'ил': 0.007, 'ем': 0.007,
    'ье': 0.007, 'тр': 0.007, 'ег': 0.007, 'ее': 0.006, 'нн': 0.006,
    'лл': 0.006, 'сс': 0.006, 'вв': 0.006, 'яя': 0.006
}


def clean_text(text):
    """Очистка текста от всех символов, кроме русских букв"""
    text = text.lower()
    text = re.sub(r'[^а-яё]', '', text)
    return text


def calculate_letter_frequencies(text):
    """Подсчет частот букв в тексте"""
    text = clean_text(text)
    total_letters = len(text)
    if total_letters == 0:
        return {}

    freq = Counter(text)
    for letter in freq:
        freq[letter] = freq[letter] / total_letters
    return freq


def calculate_bigram_frequencies(text, step=1):
    """Подсчет частот биграмм в тексте"""
    text = clean_text(text)
    bigrams = [text[i:i + 2] for i in range(0, len(text) - 1, step)]
    total_bigrams = len(bigrams)
    if total_bigrams == 0:
        return {}

    freq = Counter(bigrams)
    for bigram in freq:
        freq[bigram] = freq[bigram] / total_bigrams
    return freq


def plot_frequencies(frequencies, title, num_items=10):
    """Построение графика частот"""
    sorted_items = sorted(frequencies.items(), key=lambda x: -x[1])[:num_items]
    labels, values = zip(*sorted_items)

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel('Символы/биграммы')
    plt.ylabel('Частота')

    # Используем другой метод для отображения в PyCharm
    try:
        plt.show()
    except AttributeError:
        # Альтернативный метод для PyCharm
        plt.draw()
        plt.pause(0.001)


def analyze_large_text(filename):
    """Анализ большого текста для определения частотных характеристик"""
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    letter_freq = calculate_letter_frequencies(text)
    bigram_freq = calculate_bigram_frequencies(text)

    print("\n10 самых частых букв:")
    for letter, freq in sorted(letter_freq.items(), key=lambda x: -x[1])[:10]:
        print(f"{letter}: {freq:.4f}")

    print("\n10 самых частых биграмм:")
    for bigram, freq in sorted(bigram_freq.items(), key=lambda x: -x[1])[:10]:
        print(f"{bigram}: {freq:.4f}")

    plot_frequencies(letter_freq, "Частоты букв в тексте")
    plot_frequencies(bigram_freq, "Частоты биграмм в тексте")

    return letter_freq, bigram_freq


def caesar_brute_force(text):
    """Полный перебор для шифра Цезаря"""
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    best_shift = 0
    best_score = float('-inf')

    for shift in range(1, 33):
        decrypted = caesar_decrypt(text, shift)
        score = 0

        # Оцениваем по частотам букв
        freq = calculate_letter_frequencies(decrypted)
        for letter, prob in freq.items():
            if letter in RUSSIAN_LETTER_FREQ:
                score += prob * RUSSIAN_LETTER_FREQ[letter]

        if score > best_score:
            best_score = score
            best_shift = shift

    return best_shift


def caesar_decrypt(text, shift):
    """Расшифровка текста, зашифрованного методом Цезаря"""
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    result = []

    for char in text.lower():
        if char in alphabet:
            index = alphabet.index(char)
            new_index = (index - shift) % len(alphabet)
            result.append(alphabet[new_index])
        else:
            result.append(char)

    return ''.join(result)


def caesar_analyze(filename):
    """Криптоанализ текста, зашифрованного методом Цезаря"""
    with open(filename, 'r', encoding='utf-8') as file:
        ciphertext = file.read()

    print("\nАнализ шифра Цезаря:")
    shift = caesar_brute_force(ciphertext)
    print(f"Найденный ключ: {shift}")

    decrypted = caesar_decrypt(ciphertext, shift)
    print("\nПервые 200 символов расшифрованного текста:")
    print(decrypted[:200])

    return decrypted


def kasiski_test(ciphertext, max_key_length=20):
    """Тест Казиски для определения длины ключа Виженера"""
    # Находим повторяющиеся последовательности длиной 3-5 символов
    sequences = {}
    for length in range(3, 6):
        for i in range(len(ciphertext) - length + 1):
            seq = ciphertext[i:i + length]
            if seq in sequences:
                sequences[seq].append(i)
            else:
                sequences[seq] = [i]

    # Оставляем только последовательности, встречающиеся несколько раз
    repeated_seqs = {seq: positions for seq, positions in sequences.items() if len(positions) > 1}

    # Вычисляем расстояния между повторениями
    distances = []
    for seq, positions in repeated_seqs.items():
        for i in range(1, len(positions)):
            distances.append(positions[i] - positions[0])

    # Находим НОД всех расстояний
    if not distances:
        return 1

    current_gcd = distances[0]
    for d in distances[1:]:
        current_gcd = gcd(current_gcd, d)
        if current_gcd == 1:
            break

    # Ищем все возможные делители
    possible_lengths = set()
    for d in distances:
        for i in range(1, min(max_key_length, d) + 1):
            if d % i == 0:
                possible_lengths.add(i)

    # Считаем, сколько раз каждый делитель встречается
    length_counts = Counter()
    for d in distances:
        for l in possible_lengths:
            if d % l == 0:
                length_counts[l] += 1

    # Возвращаем наиболее вероятную длину ключа
    if not length_counts:
        return 1

    return length_counts.most_common(1)[0][0]


def friedman_test(ciphertext, max_key_length=20):
    """Тест Фридмана для определения длины ключа Виженера"""

    def index_of_coincidence(text):
        freq = Counter(text)
        total = len(text)
        if total <= 1:
            return 0.0
        return sum(f * (f - 1) for f in freq.values()) / (total * (total - 1))

    best_length = 1
    best_diff = float('inf')
    russian_ic = 0.0553  # Индекс совпадений для русского языка

    for l in range(1, max_key_length + 1):
        total_ic = 0.0
        for i in range(l):
            sequence = ciphertext[i::l]
            if len(sequence) > 1:
                total_ic += index_of_coincidence(sequence)
        avg_ic = total_ic / l
        diff = abs(avg_ic - russian_ic)

        if diff < best_diff:
            best_diff = diff
            best_length = l

    return best_length


def vigenere_find_key_length(ciphertext):
    """Определение длины ключа для шифра Виженера"""
    # Используем оба метода и выбираем наиболее вероятный результат
    kasiski_length = kasiski_test(ciphertext)
    friedman_length = friedman_test(ciphertext)

    # Если результаты совпадают или близки
    if kasiski_length == friedman_length:
        return kasiski_length
    else:
        # Предпочитаем результат Казиски, если он не 1
        return kasiski_length if kasiski_length != 1 else friedman_length


def vigenere_find_key(ciphertext, key_length):
    """Определение ключа Виженера по известной длине"""
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    key = []

    for i in range(key_length):
        sequence = ciphertext[i::key_length]
        best_shift = 0
        best_score = float('-inf')

        for shift in range(len(alphabet)):
            decrypted = [alphabet[(alphabet.index(c) - shift) % len(alphabet)] for c in sequence if c in alphabet]
            if not decrypted:
                continue

            # Оцениваем по частотам букв
            freq = Counter(decrypted)
            total = len(decrypted)
            score = 0
            for letter, count in freq.items():
                observed = count / total
                expected = RUSSIAN_LETTER_FREQ.get(letter, 0)
                score += observed * expected

            if score > best_score:
                best_score = score
                best_shift = shift

        key.append(alphabet[best_shift])

    return ''.join(key)


def vigenere_decrypt(ciphertext, key):
    """Расшифровка текста, зашифрованного методом Виженера"""
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    result = []
    key_len = len(key)

    for i, char in enumerate(ciphertext.lower()):
        if char in alphabet:
            key_char = key[i % key_len]
            shift = alphabet.index(key_char)
            index = alphabet.index(char)
            new_index = (index - shift) % len(alphabet)
            result.append(alphabet[new_index])
        else:
            result.append(char)

    return ''.join(result)


def vigenere_analyze(filename):
    """Криптоанализ текста, зашифрованного методом Виженера"""
    with open(filename, 'r', encoding='utf-8') as file:
        ciphertext = file.read()

    print("\nАнализ шифра Виженера:")

    # Определяем длину ключа
    key_length = vigenere_find_key_length(ciphertext)
    print(f"Предполагаемая длина ключа: {key_length}")

    # Определяем ключ
    key = vigenere_find_key(ciphertext, key_length)
    print(f"Предполагаемый ключ: {key}")

    # Расшифровываем текст
    decrypted = vigenere_decrypt(ciphertext, key)
    print("\nПервые 200 символов расшифрованного текста:")
    print(decrypted[:200])

    return decrypted


def main():
    print("Программа криптоанализа зашифрованных текстов")
    print("1. Анализ большого текста для определения частотных характеристик")
    print("2. Криптоанализ шифра Цезаря")
    print("3. Криптоанализ шифра Виженера")
    print("4. Выход")

    while True:
        choice = input("\nВыберите режим работы (1-4): ")

        if choice == '1':
            filename = input("Введите имя файла с большим текстом (>100000 знаков): ")
            analyze_large_text(filename)
        elif choice == '2':
            filename = input("Введите имя файла с зашифрованным текстом (Цезарь): ")
            caesar_analyze(filename)
        elif choice == '3':
            filename = input("Введите имя файла с зашифрованным текстом (Виженер): ")
            vigenere_analyze(filename)
        elif choice == '4':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()