import os
from datetime import datetime

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def print_key_matrix(matrix):
    print("\n" + "="*50)
    print("Ключевая матрица Playfair:")
    print("+" + "-"*21 + "+")
    for row in matrix:
        print("| " + " | ".join([cell.upper() for cell in row]) + " |")  # Исправлено: upper() для каждого элемента
        print("+" + "-"*21 + "+")


def toLowerCase(text):
    return text.lower()


def removeSpaces(text):
    return ''.join([char for char in text if char != ' '])


def prepareText(text):
    """Подготавливает текст к шифрованию"""
    text = removeSpaces(toLowerCase(text))
    i = 0
    while i < len(text) - 1:
        if text[i] == text[i + 1]:
            text = text[:i + 1] + 'x' + text[i + 1:]
        i += 2
    if len(text) % 2 != 0:
        text += 'z'
    return text


def createDigraphs(text):
    """Разбивает текст на пары символов (биграммы)"""
    return [text[i:i + 2] for i in range(0, len(text), 2)]


def generateKeyMatrix(key):
    """Генерирует ключевую матрицу 5x5"""
    key = toLowerCase(key)
    key_letters = []

    for char in key:
        char = 'i' if char == 'j' else char
        if char not in key_letters:
            key_letters.append(char)

    for char in ALPHABET:
        if char not in key_letters:
            key_letters.append(char)

    return [key_letters[i * 5:(i + 1) * 5] for i in range(5)]


def findPosition(matrix, char):
    """Находит позицию символа в матрице"""
    char = 'i' if char == 'j' else char
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None, None


def encryptDigraph(matrix, digraph):
    row1, col1 = findPosition(matrix, digraph[0])
    row2, col2 = findPosition(matrix, digraph[1])

    if row1 == row2:
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
    else:
        return matrix[row1][col2] + matrix[row2][col1]


def encrypt(plaintext, key):
    matrix = generateKeyMatrix(key)
    print_key_matrix(matrix)  # Показываем матрицу
    prepared_text = prepareText(plaintext)
    digraphs = createDigraphs(prepared_text)
    ciphertext = ''.join([encryptDigraph(matrix, dg) for dg in digraphs])
    return ciphertext.upper()  # Преобразуем весь результат в верхний регистр


def get_output_filename(input_path):
    dirname = os.path.dirname(input_path)
    filename, ext = os.path.splitext(os.path.basename(input_path))
    return os.path.join(dirname, f"{filename}_encrypted{ext}")


def process_file(input_file, key):
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Файл '{input_file}' не найден!")

        with open(input_file, 'r', encoding='utf-8') as f:
            plaintext = f.read()

        # Шифрование
        ciphertext = encrypt(plaintext, key)
        output_file = get_output_filename(input_file)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ciphertext)

        # Вывод первых 200 символов
        preview = ciphertext[:200]
        if len(ciphertext) > 200:
            preview += "..."

        print("="*50)
        print("Первые 200 символов зашифрованного текста:")
        print(preview)

    except Exception as e:
        print(f"\nОшибка: {str(e)}")


if __name__ == "__main__":
    print("Шифр Playfair")
    print("="*50)

    input_file = input("Введите путь к исходному файлу: ").strip()
    key = input("Введите ключевое слово: ").strip()

    process_file(input_file, key)