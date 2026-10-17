import random

from src.MathTrainer.core.task import Task


def addition_generators(limit: int) -> Task:
    """Генерирует примеры на сложение в заданном диапозоне limit"""
    ans = random.randint(1, limit)
    a = random.randint(0, ans)
    b = ans - a
    return Task(text=f"{a} + {b} = ?", answer=ans)
