import random


def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():  # Проверяем, является ли символ буквой
            shift_amount = shift % 33
            if char == 'Ё':
                result += chr(((ord('Е') - ord('А') + shift_amount) % 33 + ord('А')))
            elif char == 'ё':
                result += chr(((ord('е') - ord('а') + shift_amount) % 33 + ord('а')))
            elif char.islower():
                result += chr(((ord(char) - ord('а') + shift_amount) % 33 + ord('а')))
            else:
                result += chr(((ord(char) - ord('А') + shift_amount) % 33 + ord('А')))
        else:
            result += char
    return result


def generate_vigenere_square():
    square = []
    for i in range(33):
        square.append([chr((i + j) % 33 + ord('А')) for j in range(33)])
    return square


def vigenere_cipher(text, key, alphabet_choice):
    if alphabet_choice == 'random':
        alphabet = list('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
        random.shuffle(alphabet)
    else:
        alphabet = list('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')

    square = generate_vigenere_square()
    key_length = len(key)
    key_as_int = [ord(i.upper()) - ord('А') for i in key]
    text_as_int = [ord(i.upper()) - ord('А') if i.isalpha() else i for i in text]
    result = ""
    for i in range(len(text_as_int)):
        if isinstance(text_as_int[i], int):
            shift = key_as_int[i % key_length]
            result += square[shift][text_as_int[i]]
        else:
            result += text_as_int[i]
    return result


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def main():
    mode = input("Выберите режим (1 - Цезарь, 2 - Виженер): ")
    filename = input("Введите имя файла: ")
    text = read_file(filename + ".txt")

    if mode == '1':
        shift = int(input("Введите ключ для шифра Цезаря: "))
        encrypted_text = caesar_cipher(text, shift)
        write_file("encC_" + filename + ".txt", encrypted_text)
        decrypted_text = caesar_cipher(encrypted_text, -shift)
        write_file("decC_" + filename + ".txt", decrypted_text)
        print("Первые строки файлов:")
        print("Исходный текст:", text[:100])
        print("Зашифрованный текст:", encrypted_text[:100])
        print("Расшифрованный текст:", decrypted_text[:100])
    elif mode == '2':
        key = input("Введите ключ для шифра Виженера: ")
        alphabet_choice = input("Выберите алфавит (random - случайный, order - по порядку): ")
        encrypted_text = vigenere_cipher(text, key, alphabet_choice)
        write_file("encV_" + filename + ".txt", encrypted_text)
        decrypted_text = vigenere_cipher(encrypted_text, key, alphabet_choice)
        write_file("decV_" + filename + ".txt", decrypted_text)
        print("Первые строки файлов:")
        print("Исходный текст:", text[:100])
        print("Зашифрованный текст:", encrypted_text[:100])
        print("Расшифрованный текст:", decrypted_text[:100])


if __name__ == "__main__":
    main()