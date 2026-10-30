import math
import random

from src.MathTrainer.core.task import Task

PREFIX = "Реши уравнение: "
LIMITS = [100, 1000]


def _task(equation: str, answer: int) -> Task:
    return Task(text=f"{PREFIX}{equation}", answer=answer)


def _side(limit: int) -> int:
    return math.isqrt(limit)


#сложение / вычитание

def x_plus_a(limit):          # x + a = c
    x = random.randint(0, limit)
    a = random.randint(0, limit - x)
    return _task(f"x + {a} = {x + a}", x)


def x_minus_a(limit):         # x - a = b
    x = random.randint(0, limit)
    a = random.randint(0, x)
    return _task(f"x - {a} = {x - a}", x)


def a_plus_x(limit):          # a + x = c
    x = random.randint(0, limit)
    a = random.randint(0, limit - x)
    return _task(f"{a} + x = {x + a}", x)


def a_minus_x(limit):         # a - x = b
    a = random.randint(0, limit)
    x = random.randint(0, a)
    return _task(f"{a} - x = {a - x}", x)


def x_plus_a_minus_b(limit):  # x + a - b = c
    x = random.randint(0, limit)
    a = random.randint(0, limit - x)
    b = random.randint(0, x + a)
    return _task(f"x + {a} - {b} = {x + a - b}", x)


def x_minus_a_plus_b(limit):  # x - a + b = c
    x = random.randint(0, limit)
    a = random.randint(0, x)
    b = random.randint(0, limit - (x - a))
    return _task(f"x - {a} + {b} = {x - a + b}", x)


def a_plus_x_plus_b(limit):   # a + x + b = c
    x = random.randint(0, limit)
    a = random.randint(0, limit - x)
    b = random.randint(0, limit - x - a)
    return _task(f"{a} + x + {b} = {x + a + b}", x)


def a_plus_x_minus_b(limit):  # a + x - b = c
    x = random.randint(0, limit)
    a = random.randint(0, limit - x)
    b = random.randint(0, x + a)
    return _task(f"{a} + x - {b} = {x + a - b}", x)


ADD_SUB = [
    x_plus_a, x_minus_a, a_plus_x, a_minus_x,
    x_plus_a_minus_b, x_minus_a_plus_b, a_plus_x_plus_b, a_plus_x_minus_b,
]


#умножение / деление

def a_times_x(limit):         # a × x = c
    side = _side(limit)
    a, x = random.randint(1, side), random.randint(0, side)
    return _task(f"{a} × x = {a * x}", x)


def x_times_a(limit):         # x × a = c
    side = _side(limit)
    a, x = random.randint(1, side), random.randint(0, side)
    return _task(f"x × {a} = {a * x}", x)


def x_div_a(limit):           # x ÷ a = b
    side = _side(limit)
    a, b = random.randint(1, side), random.randint(0, side)
    return _task(f"x ÷ {a} = {b}", a * b)


def a_div_x(limit):           # c ÷ x = b   (b >= 1, иначе 0 ÷ x = 0 подходит любому x)
    side = _side(limit)
    x, b = random.randint(1, side), random.randint(1, side)
    return _task(f"{x * b} ÷ x = {b}", x)


MUL_DIV = [a_times_x, x_times_a, x_div_a, a_div_x]


#смешанные

def x_times_m_plus_k(limit):   # x × m + k = r
    side = _side(limit)
    m, x = random.randint(2, side), random.randint(0, side)
    k = random.randint(0, limit - x * m)
    return _task(f"x × {m} + {k} = {x * m + k}", x)


def x_times_m_minus_k(limit):  # x × m - k = r
    side = _side(limit)
    m, x = random.randint(2, side), random.randint(0, side)
    k = random.randint(0, x * m)
    return _task(f"x × {m} - {k} = {x * m - k}", x)


MIX = [x_times_m_plus_k, x_times_m_minus_k]




def _pick(patterns, limit):
    if limit is None:
        limit = random.choice(LIMITS)
    return random.choice(patterns)(limit)


def equations_add_sub(limit=None):
    """Уравнения на сложение и вычитание"""
    return _pick(ADD_SUB, limit)


def equations_mul_div(limit=None):
    """Уравнения на умножение и деление"""
    return _pick(MUL_DIV, limit)


def equations_mix(limit=None):
    """Уравнения в два действия (× и +/-)"""
    return _pick(MIX, limit)


def equations_all(limit=None):
    """Все типы уравнений"""
    return _pick(ADD_SUB + MUL_DIV + MIX, limit)