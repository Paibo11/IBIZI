import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import time
import itertools
import string
import math

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

def validate_password(password, restrictions):
    if restrictions:
        min_length = restrictions.get('min_length', 0)
        if min_length is None:
            min_length = 0
        if 'min_length' in restrictions and len(password) < min_length:
            return False, f"Пароль должен быть не менее {min_length} символов."
        if 'uppercase' in restrictions and restrictions['uppercase'] and not any(c.isupper() for c in password):
            return False, "Пароль должен содержать хотя бы одну заглавную букву."
        if 'lowercase' in restrictions and restrictions['lowercase'] and not any(c.islower() for c in password):
            return False, "Пароль должен содержать хотя бы одну строчную букву."
        if 'digits' in restrictions and restrictions['digits'] and not any(c.isdigit() for c in password):
            return False, "Пароль должен содержать хотя бы одну цифру."
        if 'special_chars' in restrictions and restrictions['special_chars'] and not any(c in r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""" for c in password):
            return False, "Пароль должен содержать хотя бы один специальный символ."
    return True, "Пароль соответствует требованиям."

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

def calculate(password, s):
    N = get_alphabet_power(password)
    L = len(password)
    M = N ** L

    base_time = M / s
    total_time = base_time

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

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Вход в систему")
        self.root.geometry("300x250")
        self.user_data = load_user_data()
        self.attempts = 0

        self.username_label = tk.Label(root, text="Имя пользователя:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Пароль:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Войти", command=self.login)
        self.login_button.pack()

        self.brute_force_button = tk.Button(root, text="Подобрать пароль", command=self.brute_force_password)
        self.brute_force_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username not in self.user_data:
            messagebox.showerror("Ошибка", "Пользователь не найден")
            return

        if self.user_data[username]['blocked']:
            messagebox.showerror("Ошибка", "Ваш аккаунт заблокирован")
            return

        if self.user_data[username]['password'] != password:
            self.attempts += 1
            if self.attempts >= 3:
                messagebox.showerror("Ошибка", "Превышено количество попыток")
                self.root.quit()
            else:
                messagebox.showerror("Ошибка", f"Неверный пароль. Осталось попыток: {3 - self.attempts}")
            return

        self.root.destroy()
        if username == 'ADMIN':
            admin_root = tk.Tk()
            admin_root.geometry("400x300")
            AdminApp(admin_root, self.user_data)
        else:
            user_root = tk.Tk()
            user_root.geometry("200x100")
            UserApp(user_root, username, self.user_data)

    def brute_force_password(self):
        username = self.username_entry.get()
        if username not in self.user_data:
            messagebox.showerror("Ошибка", "Пользователь не найден")
            return

        if self.user_data[username]['blocked']:
            messagebox.showerror("Ошибка", "Ваш аккаунт заблокирован")
            return

        method = simpledialog.askstring("Метод подбора", "Выберите метод подбора (dictionary/full):")
        if method == "d":
            dictionary = ["admin", "password", "123456", "qwerty", "1!!qqW"]
            start_time = time.time()
            for word in dictionary:
                if word == self.user_data[username]['password']:
                    elapsed_time = time.time() - start_time
                    self.password_entry.delete(0, tk.END)
                    self.password_entry.insert(0, word)
                    messagebox.showinfo("Успех", f"Пароль подобран: {word}\nВремя подбора: {elapsed_time:.2f} секунд")
                    return
            messagebox.showerror("Ошибка", "Пароль не найден в словаре")
        elif method == "f":
            password = self.user_data[username]['password']
            s = float(simpledialog.askstring("Скорость", "Введите скорость перебора паролей в секунду:"))
            calculateTime = calculate(password, s)
            formatted_time = format_time(calculateTime)
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            messagebox.showinfo("Оценочное время", f"Оценочное время перебора пароля: {formatted_time}\nНайденный пароль: {password}")
        else:
            messagebox.showerror("Ошибка", "Неверный метод подбора")

class AdminApp:
    def __init__(self, root, user_data):
        self.root = root
        self.root.title("Режим администратора")
        self.user_data = user_data

        self.change_password_button = tk.Button(root, text="Сменить пароль администратора", command=self.change_password)
        self.change_password_button.pack()

        self.view_users_button = tk.Button(root, text="Просмотреть список пользователей", command=self.view_users)
        self.view_users_button.pack()

        self.add_user_button = tk.Button(root, text="Добавить нового пользователя", command=self.add_user)
        self.add_user_button.pack()

        self.block_user_button = tk.Button(root, text="Блокировать пользователя", command=self.block_user)
        self.block_user_button.pack()

        self.unblock_user_button = tk.Button(root, text="Разблокировать пользователя", command=self.unblock_user)
        self.unblock_user_button.pack()

        self.set_restrictions_button = tk.Button(root, text="Задать ограничения на пароль", command=self.set_restrictions)
        self.set_restrictions_button.pack()

        self.remove_restrictions_button = tk.Button(root, text="Снять ограничения на пароль", command=self.remove_restrictions)
        self.remove_restrictions_button.pack()

        self.exit_button = tk.Button(root, text="Выйти", command=self.logout)
        self.exit_button.pack()

    def change_password(self):
        old_password = simpledialog.askstring("Смена пароля", "Введите старый пароль:", show='*')
        if old_password == self.user_data['ADMIN']['password']:
            new_password = simpledialog.askstring("Смена пароля", "Введите новый пароль:", show='*')
            confirm_password = simpledialog.askstring("Смена пароля", "Подтвердите новый пароль:", show='*')
            if new_password == confirm_password:
                if self.user_data['ADMIN']['password_restrictions']:
                    is_valid, message = validate_password(new_password, self.user_data['ADMIN']['password_restrictions'])
                    if not is_valid:
                        messagebox.showerror("Ошибка", message)
                        return
                self.user_data['ADMIN']['password'] = new_password
                save_user_data(self.user_data)
                messagebox.showinfo("Успех", "Пароль успешно изменен")
            else:
                messagebox.showerror("Ошибка", "Пароли не совпадают")
        else:
            messagebox.showerror("Ошибка", "Неверный старый пароль")

    def view_users(self):
        users_info = "\n".join([f"Пользователь: {user}, Блокирован: {info['blocked']}, Ограничения: {info['password_restrictions']}" for user, info in self.user_data.items()])
        messagebox.showinfo("Список пользователей", users_info)

    def add_user(self):
        new_user = simpledialog.askstring("Добавить пользователя", "Введите имя нового пользователя:")
        if new_user in self.user_data:
            messagebox.showerror("Ошибка", "Пользователь уже существует")
        else:
            self.user_data[new_user] = {'password': '', 'blocked': False, 'password_restrictions': None}
            save_user_data(self.user_data)
            messagebox.showinfo("Успех", "Пользователь добавлен")

    def block_user(self):
        user_to_block = simpledialog.askstring("Блокировать пользователя", "Введите имя пользователя для блокировки:")
        if user_to_block in self.user_data:
            self.user_data[user_to_block]['blocked'] = True
            save_user_data(self.user_data)
            messagebox.showinfo("Успех", "Пользователь заблокирован")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")

    def unblock_user(self):
        user_to_unblock = simpledialog.askstring("Разблокировать пользователя", "Введите имя пользователя для разблокировки:")
        if user_to_unblock in self.user_data:
            self.user_data[user_to_unblock]['blocked'] = False
            save_user_data(self.user_data)
            messagebox.showinfo("Успех", "Пользователь разблокирован")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")

    def set_restrictions(self):
        user_to_set = simpledialog.askstring("Задать ограничения", "Введите имя пользователя:")
        if user_to_set in self.user_data:
            restrictions = {}
            min_length = simpledialog.askinteger("Ограничения", "Минимальная длина пароля:", initialvalue=8)
            if min_length is None:
                min_length = 0
            restrictions['min_length'] = min_length
            restrictions['uppercase'] = messagebox.askyesno("Ограничения", "Требовать заглавные буквы?")
            restrictions['lowercase'] = messagebox.askyesno("Ограничения", "Требовать строчные буквы?")
            restrictions['digits'] = messagebox.askyesno("Ограничения", "Требовать цифры?")
            restrictions['special_chars'] = messagebox.askyesno("Ограничения", "Требовать специальные символы?")
            self.user_data[user_to_set]['password_restrictions'] = restrictions
            save_user_data(self.user_data)
            messagebox.showinfo("Успех", f"Ограничения для пользователя {user_to_set} заданы: {restrictions}")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")

    def remove_restrictions(self):
        user_to_remove = simpledialog.askstring("Снять ограничения", "Введите имя пользователя:")
        if user_to_remove in self.user_data:
            self.user_data[user_to_remove]['password_restrictions'] = None
            save_user_data(self.user_data)
            messagebox.showinfo("Успех", f"Ограничения для пользователя {user_to_remove} сняты.")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        app = LoginApp(root)
        root.mainloop()

class UserApp:
    def __init__(self, root, username, user_data):
        self.root = root
        self.root.title("Режим пользователя")
        self.username = username
        self.user_data = user_data

        self.change_password_button = tk.Button(root, text="Сменить пароль", command=self.change_password)
        self.change_password_button.pack()

        self.exit_button = tk.Button(root, text="Выйти", command=self.logout)
        self.exit_button.pack()

    def change_password(self):
        old_password = simpledialog.askstring("Смена пароля", "Введите старый пароль:", show='*')
        if old_password == self.user_data[self.username]['password']:
            new_password = simpledialog.askstring("Смена пароля", "Введите новый пароль:", show='*')
            confirm_password = simpledialog.askstring("Смена пароля", "Подтвердите новый пароль:", show='*')
            if new_password == confirm_password:
                if self.user_data[self.username]['password_restrictions']:
                    is_valid, message = validate_password(new_password, self.user_data[self.username]['password_restrictions'])
                    if not is_valid:
                        messagebox.showerror("Ошибка", message)
                        return
                self.user_data[self.username]['password'] = new_password
                save_user_data(self.user_data)
                messagebox.showinfo("Успех", "Пароль успешно изменен")
            else:
                messagebox.showerror("Ошибка", "Пароли не совпадают")
        else:
            messagebox.showerror("Ошибка", "Неверный старый пароль")

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        app = LoginApp(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
