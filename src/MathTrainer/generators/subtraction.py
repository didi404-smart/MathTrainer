import random

from src.MathTrainer.core.task import Task


def subtraction_generators(limit: int) -> Task:
    """Генерирует примеры на вычитания в заданном диапозоне limit"""
    a = random.randint(1, limit)
    b = random.randint(0, a)
    return Task(text=f"{a} - {b} = ?", answer=a - b)
