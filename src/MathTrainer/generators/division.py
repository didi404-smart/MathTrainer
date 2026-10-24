import random
from src.MathTrainer.core.task import Task


def division(quot_limit: int, b_min: int, b_max: int) -> Task:
    """Генерирует примеры на деление"""
    a = random.randint(0, quot_limit)
    b = random.randint(b_min, b_max)
    return Task(text=f"Выполни деление без остатка: {a * b} ÷ {b} = ?", answer=a)


def division_table_10_10() -> Task:
    return division(10, 1, 10)


def division_one_digit() -> Task:
    return division(1000, 1, 9)


def division_two_digit() -> Task:
    return division(1000, 10, 99)


def division_three_digit() -> Task:
    return division(200, 100, 999)


def division_all() -> Task:
    return division(1000, 1, 999)