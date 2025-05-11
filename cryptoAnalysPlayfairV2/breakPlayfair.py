import playfairCipher
import datetime
import random
import pickle
import math
import os
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from threading import Thread

LETTERS = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K',
           'J', 'X', 'Q', 'Z']
FREQUENCY = [0.12702, 0.09056, 0.08167, 0.07507, 0.06966, 0.06749, 0.06327, 0.06094, 0.05987, 0.04253, 0.04025, 0.02782,
             0.02758, 0.02406, 0.02360, 0.02228, 0.02015, 0.01974, 0.01929, 0.01492, 0.00978, 0.00772, 0.00153, 0.00150,
             0.00095, 0.00074]
ENGLISH_FREQUENCY = dict(zip(LETTERS, FREQUENCY))

# Загрузка триграмм
with open('trigrams', 'rb') as f:
    ENGLISH_TRIGRAMS = pickle.load(f)

# Кеширование дешифровок
DECRYPT_CACHE = {}


class CipherBreakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Взломщик шифра Плейфера")
        self.root.geometry("600x450")

        self.running = False
        self.current_process = None
        self.total_iterations = 0
        self.current_iteration = 0

        self.create_widgets()

    def create_widgets(self):
        # Файл для расшифровки
        tk.Label(self.root, text="Файл для расшифровки:").pack(pady=(10, 0))

        self.file_frame = tk.Frame(self.root)
        self.file_frame.pack(pady=5)

        self.file_entry = tk.Entry(self.file_frame, width=40)
        self.file_entry.pack(side=tk.LEFT, padx=5)

        self.browse_btn = tk.Button(self.file_frame, text="Обзор...", command=self.browse_file)
        self.browse_btn.pack(side=tk.LEFT)

        # Кнопки управления
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        self.break_btn = tk.Button(self.btn_frame, text="Взломать шифр", command=self.start_breaking)
        self.break_btn.pack(side=tk.LEFT, padx=5)

        self.cancel_btn = tk.Button(self.btn_frame, text="Отмена", state=tk.DISABLED, command=self.cancel_breaking)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)

        # Прогресс бар
        self.progress_label = tk.Label(self.root, text="Прогресс: 0%")
        self.progress_label.pack(pady=(10, 0))

        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=5)

        # Статус
        self.status_label = tk.Label(self.root, text="Готов к работе")
        self.status_label.pack(pady=5)

        # Результаты
        self.result_frame = tk.LabelFrame(self.root, text="Результаты")
        self.result_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(self.result_frame, height=8, wrap=tk.WORD)
        self.result_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)

    def start_breaking(self):
        if not self.file_entry.get():
            messagebox.showerror("Ошибка", "Выберите файл для расшифровки")
            return

        self.running = True
        self.break_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.status_label.config(text="Взлом шифра...")
        self.progress['value'] = 0
        self.progress_label.config(text="Прогресс: 0%")

        # Запуск в отдельном потоке
        self.current_process = Thread(target=self.break_cipher_thread)
        self.current_process.start()

    def cancel_breaking(self):
        self.running = False
        self.status_label.config(text="Отмена...")

    def update_progress(self, current, total):
        progress = int((current / total) * 100)
        self.progress['value'] = progress
        self.progress_label.config(text=f"Прогресс: {progress}%")
        self.root.update_idletasks()

    def break_cipher_thread(self):
        try:
            input_file = self.file_entry.get()
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_decrypted.txt"

            # Чтение файла
            message = playfairCipher.readfile(input_file)
            key = playfairCipher.Playfair.buildtable('CHARITY')
            ciphertext = playfairCipher.Playfair.encrypt(message, key)

            self.append_result("--- Взлом шифра Плейфера ---\n")
            self.append_result(f"Зашифрованный текст (первые 100 символов): {ciphertext[:100]}...\n")
            self.append_result(f"Оценка триграмм для зашифрованного текста: {log_trigram_fitness(ciphertext)}\n\n")

            # Настройки для прогресс-бара
            restarts = 20
            max_iter = 20000
            self.total_iterations = restarts * max_iter
            self.current_iteration = 0

            best_text, best_key, best_score = self.simulated_annealing(ciphertext, max_iter, restarts)

            # Сохранение результатов в тот же каталог
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(best_text)

            self.append_result("\n--- Лучший результат ---\n")
            self.append_result(f"Ключ: {best_key}\n")
            self.append_result(f"Оценка: {best_score}\n")
            self.append_result(f"Расшифрованный текст сохранен в: {output_file}\n")
            self.append_result(f"Первые 200 символов:\n{best_text[:200]}...\n")

            self.status_label.config(text="Готово")
            messagebox.showinfo("Готово", f"Расшифрованный текст сохранен в файл:\n{output_file}")

        except Exception as e:
            self.append_result(f"Ошибка: {str(e)}\n")
            self.status_label.config(text="Ошибка")
            messagebox.showerror("Ошибка", str(e))
        finally:
            self.running = False
            self.break_btn.config(state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)
            self.progress['value'] = 100
            self.progress_label.config(text="Прогресс: 100%")

    def simulated_annealing(self, ciphertext, max_iter, restarts):
        best_key = None
        best_score = -float('inf')
        best_decrypted = ""

        for i in range(restarts):
            if not self.running:
                break

            current_key = ''.join(random.sample(playfairCipher.ALPHABET.replace('J', ''), 25))
            current_score = log_trigram_fitness(playfairCipher.Playfair.decrypt(ciphertext, current_key))

            T = 10.0
            cooling_rate = 0.9995

            for j in range(max_iter):
                if not self.running:
                    break

                self.current_iteration = i * max_iter + j
                self.update_progress(self.current_iteration, self.total_iterations)

                new_key = playfair_key_transformation(current_key)

                if new_key in DECRYPT_CACHE:
                    decrypted = DECRYPT_CACHE[new_key]
                else:
                    decrypted = playfairCipher.Playfair.decrypt(ciphertext, new_key)
                    DECRYPT_CACHE[new_key] = decrypted

                new_score = log_trigram_fitness(decrypted)

                if new_score > best_score:
                    best_score = new_score
                    best_key = new_key
                    best_decrypted = decrypted

                if new_score > current_score or random.random() < math.exp((new_score - current_score) / T):
                    current_score = new_score
                    current_key = new_key

                T *= cooling_rate

        return best_decrypted, best_key, best_score

    def append_result(self, text):
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)
        self.root.update_idletasks()


def count_trigrams(text):
    return max(1, len(text) - 2)


def trigram_frequency(text, trigram):
    return text.count(trigram) / count_trigrams(text)


def log_trigram_fitness(text):
    score = 0.0
    for trigram, prob in ENGLISH_TRIGRAMS.items():
        freq = trigram_frequency(text, trigram)
        if freq > 0 and prob > 0:
            score += freq * math.log(prob)
    return score


def playfair_key_transformation(key):
    key = list(key)
    mutation_type = random.choices(
        ["swap_letters", "swap_rows", "swap_cols", "reverse", "transpose"],
        weights=[0.8, 0.05, 0.05, 0.05, 0.05],
        k=1
    )[0]

    if mutation_type == "swap_letters":
        i, j = random.sample(range(25), 2)
        key[i], key[j] = key[j], key[i]
    elif mutation_type == "swap_rows":
        i, j = random.sample(range(5), 2)
        for k in range(5):
            key[i * 5 + k], key[j * 5 + k] = key[j * 5 + k], key[i * 5 + k]
    elif mutation_type == "swap_cols":
        i, j = random.sample(range(5), 2)
        for k in range(5):
            key[k * 5 + i], key[k * 5 + j] = key[k * 5 + j], key[k * 5 + i]
    elif mutation_type == "reverse":
        key.reverse()
    elif mutation_type == "transpose":
        new_key = [key[j * 5 + i] for i in range(5) for j in range(5)]
        key = new_key
    return ''.join(key)


if __name__ == "__main__":
    root = tk.Tk()
    app = CipherBreakerApp(root)
    root.mainloop()