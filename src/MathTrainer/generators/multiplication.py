import random

from src.MathTrainer.core.task import Task


def multiplication_table_10_10() -> Task:
    a = random.randint(0, 10)
    b = random.randint(0, 10)
    return Task(text=f"Выполни умножение {a} × {b} = ?", answer=a * b)


def multiplication_one_digit() -> Task:
    a = random.randint(10, 100000)
    b = random.randint(0, 9)
    return Task(text=f"Выполни умножение(столбиком) {a} × {b} = ?", answer=a * b)


def multiplication_two_digit() -> Task:
    a = random.randint(10, 100000)
    b = random.randint(10, 99)
    return Task(text=f"Выполни умножение(столбиком) {a} × {b} = ?", answer=a * b)


def multiplication_three_digit() -> Task:
    a = random.randint(100, 100000)
    b = random.randint(100, 999)
    return Task(text=f"Выполни умножение(столбиком) {a} × {b} = ?", answer=a * b)


def multiplication_four_digit() -> Task:
    a = random.randint(1000, 100000)
    b = random.randint(1000, 9999)
    return Task(text=f"Выполни умножение(столбиком) {a} × {b} = ?", answer=a * b)


def multiplication_all() -> Task:
    a = random.randint(0, 100000)
    b = random.randint(0, 9999)
    return Task(text=f"Выполни умножение(столбиком) {a} × {b} = ?", answer=a * b)
