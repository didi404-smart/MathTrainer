import random

from src.core.task import Task


def addition_generators(limit: int) -> Task:
    """Функция на вход получает диапозон(лимит), генерирует пример и ответ. Возвращает класс Task"""
    ans = random.randint(1, limit)
    a = random.randint(0, ans)
    b = ans - a
    return Task(text=f"{a} + {b} = ?", answer=ans)


print(addition_generators(20))
