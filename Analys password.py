import itertools
import string
import math


def get_alphabet_power(password):
    alphabet = 0
    if any(c.islower() for c in password):
        alphabet += 26
    if any(c.isupper() for c in password):
        alphabet += 26
    if any(c.isdigit() for c in password):
        alphabet += 10
    if any(c in string.punctuation for c in password):
        alphabet += len(string.punctuation)
    return alphabet


def calculate(password, s, m, v):
    N = get_alphabet_power(password)
    L = len(password)
    M = N ** L

    # Время перебора без пауз
    base_time = M / s

    # Учитываем паузы после m попыток
    pause_time = (M / m) * v
    total_time = base_time + pause_time

    print(f'Мощность алфавита: {M}');
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


# Ввод данных
password = input("Введите пароль: ")
s = float(input("Введите скорость перебора паролей в секунду: "))
m = int(input("Введите количество неправильных попыток перед паузой: "))
v = float(input("Введите длительность паузы в секундах: "))

# Расчет времени взлома
calculateTime = calculate(password, s, m, v)
formatted_time = format_time(calculateTime)

print(f"Оценочное время перебора пароля: {formatted_time}")