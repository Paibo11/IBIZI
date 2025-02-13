import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

USER_DATA_FILE = 'user_data.json'

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {'ADMIN': {'password': '', 'blocked': False, 'password_restrictions': False}}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file)

def validate_password(password):
    return len(password) >= 8

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Вход в систему")
        self.root.geometry("300x250")
        self.user_data = load_user_data()

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
            messagebox.showerror("Ошибка", "Неверный пароль")
            return

        self.root.destroy()
        if username == 'ADMIN':
            admin_root = tk.Tk()
            admin_root.geometry("300x220")
            AdminApp(admin_root, self.user_data)
        else:
            user_root = tk.Tk()
            user_root.geometry("400x200")
            UserApp(user_root, username, self.user_data)

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

        self.toggle_restrictions_button = tk.Button(root, text="Включить/отключить ограничения на пароли", command=self.toggle_restrictions)
        self.toggle_restrictions_button.pack()

        self.exit_button = tk.Button(root, text="Завершить работу", command=root.quit)
        self.exit_button.pack()

    def change_password(self):
        old_password = simpledialog.askstring("Смена пароля", "Введите старый пароль:", show='*')
        if old_password == self.user_data['ADMIN']['password']:
            new_password = simpledialog.askstring("Смена пароля", "Введите новый пароль:", show='*')
            confirm_password = simpledialog.askstring("Смена пароля", "Подтвердите новый пароль:", show='*')
            if new_password == confirm_password:
                self.user_data['ADMIN']['password'] = new_password
                save_user_data(self.user_data)
                messagebox.showinfo("Успех", "Пароль успешно изменен")
            else:
                messagebox.showerror("Ошибка", "Пароли не совпадают")
        else:
            messagebox.showerror("Ошибка", "Неверный старый пароль")

    def view_users(self):
        users_info = "\n".join([f"Пользователь: {user}, Блокирован: {info['blocked']}, Ограничения на пароль: {info['password_restrictions']}" for user, info in self.user_data.items()])
        messagebox.showinfo("Список пользователей", users_info)

    def add_user(self):
        new_user = simpledialog.askstring("Добавить пользователя", "Введите имя нового пользователя:")
        if new_user in self.user_data:
            messagebox.showerror("Ошибка", "Пользователь уже существует")
        else:
            self.user_data[new_user] = {'password': '', 'blocked': False, 'password_restrictions': False}
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

    def toggle_restrictions(self):
        user_to_toggle = simpledialog.askstring("Ограничения на пароль", "Введите имя пользователя для изменения ограничений на пароль:")
        if user_to_toggle in self.user_data:
            self.user_data[user_to_toggle]['password_restrictions'] = not self.user_data[user_to_toggle]['password_restrictions']
            save_user_data(self.user_data)
            messagebox.showinfo("Успех", "Ограничения на пароль изменены")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")

class UserApp:
    def __init__(self, root, username, user_data):
        self.root = root
        self.root.title("Режим пользователя")
        self.username = username
        self.user_data = user_data

        self.change_password_button = tk.Button(root, text="Сменить пароль", command=self.change_password)
        self.change_password_button.pack()

        self.exit_button = tk.Button(root, text="Завершить работу", command=root.quit)
        self.exit_button.pack()

    def change_password(self):
        old_password = simpledialog.askstring("Смена пароля", "Введите старый пароль:", show='*')
        if old_password == self.user_data[self.username]['password']:
            new_password = simpledialog.askstring("Смена пароля", "Введите новый пароль:", show='*')
            confirm_password = simpledialog.askstring("Смена пароля", "Подтвердите новый пароль:", show='*')
            if new_password == confirm_password:
                if self.user_data[self.username]['password_restrictions'] and not validate_password(new_password):
                    messagebox.showerror("Ошибка", "Пароль не соответствует требованиям")
                    return
                self.user_data[self.username]['password'] = new_password
                save_user_data(self.user_data)
                messagebox.showinfo("Успех", "Пароль успешно изменен")
            else:
                messagebox.showerror("Ошибка", "Пароли не совпадают")
        else:
            messagebox.showerror("Ошибка", "Неверный старый пароль")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()