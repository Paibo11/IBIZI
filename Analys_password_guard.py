import itertools
import string
import math
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import time

USER_DATA_FILE = 'user_data.json'

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {'ADMIN': {'password': 'admin123', 'blocked': False, 'password_restrictions': None}}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def get_alphabet_power(password):
    alphabet = 0

    if any('а' <= c <= 'я' for c in password):
        alphabet += 26
    if any('А' <= c <= 'Я' for c in password):
        alphabet += 26
    if any('a' <= c <= 'z' for c in password):
        alphabet += 33
    if any('A' <= c <= 'Z' for c in password):
        alphabet += 33
    if any(c.isdigit() for c in password):
        alphabet += 10
    if any(c in string.punctuation for c in password):
        alphabet += len(string.punctuation)
    return alphabet

def calculate(password, s, m, v):
    N = get_alphabet_power(password)
    L = len(password)
    M = N ** L

    base_time = M / s
    pause_time = ((M-1) / m) * v
    total_time = base_time + pause_time

    print(f'Мощность алфавита: {N}')
    print(f'Количество комбинаций: {M}')
    return total_time

def format_time(seconds):
    years = seconds // (365 * 24 * 3600)
    seconds %= (365 * 24 * 3600)
    months = seconds // (30 * 24 * 3600)
    seconds %= (30 * 24 * 3600)
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{int(years)} лет {int(months)} месяцев {int(days)} дней {int(hours)} часов {int(minutes)} минут {int(seconds)} секунд"

def dictionary_attack(password, dictionary):
    start_time = time.time()
    for word in dictionary:
        if word == password:
            return True, time.time() - start_time
    return False, time.time() - start_time

def brute_force_attack(password, max_length):
    chars = string.ascii_letters + string.digits + string.punctuation
    start_time = time.time()
    attempts = 0

    for length in range(1, max_length + 1):
        for attempt in itertools.product(chars, repeat=length):
            attempts += 1
            attempt = ''.join(attempt)
            if attempt == password:
                return True, time.time() - start_time, attempts
            # Прерываем, если прошло слишком много времени (например, 10 секунд)
            if time.time() - start_time > 100:
                return False, time.time() - start_time, attempts
    return False, time.time() - start_time, attempts

class PasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Программа проверки и подбора пароля")
        self.root.geometry("400x300")
        self.user_data = load_user_data()

        self.mode_label = tk.Label(root, text="Выберите режим:")
        self.mode_label.pack()

        self.check_password_button = tk.Button(root, text="Проверить надежность пароля", command=self.check_password)
        self.check_password_button.pack()

        self.crack_password_button = tk.Button(root, text="Подобрать пароль ADMIN", command=self.crack_password)
        self.crack_password_button.pack()

    def check_password(self):
        password = simpledialog.askstring("Проверка надежности пароля", "Введите пароль:")
        s = float(simpledialog.askstring("Проверка надежности пароля", "Введите скорость перебора паролей в секунду:"))
        m = int(simpledialog.askstring("Проверка надежности пароля", "Введите количество неправильных попыток перед паузой:"))
        v = float(simpledialog.askstring("Проверка надежности пароля", "Введите длительность паузы в секундах:"))

        calculateTime = calculate(password, s, m, v)
        formatted_time = format_time(calculateTime)
        messagebox.showinfo("Результат", f"Оценочное время перебора пароля: {formatted_time}")

    def crack_password(self):
        dictionary = ["password", "123456", "admin123", "qwerty", "gfhjkm"]  # Пример словаря
        max_length = 6  # Максимальная длина пароля для перебора

        password = self.user_data['ADMIN']['password']
        success, time_taken = dictionary_attack(password, dictionary)
        if success:
            messagebox.showinfo("Результат", f"Пароль подобран по словарю за {time_taken:.2f} секунд.")
            return

        success, time_taken, attempts = brute_force_attack(password, max_length)
        if success:
            messagebox.showinfo("Результат", f"Пароль подобран перебором за {time_taken:.2f} секунд. Попыток: {attempts}")
        else:
            messagebox.showinfo("Результат", f"Пароль не удалось подобрать. Попыток: {attempts}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()