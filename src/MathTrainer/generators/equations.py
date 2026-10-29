import random

from src.MathTrainer.core.task import Task

PREFIX = "Реши уравнение: "


def _task(equation: str, answer: int) -> Task:
    return Task(text=f"{PREFIX}{equation}", answer=answer)


# сложение / вычитание


def x_plus_a():  # x + a = c
    x, a = random.randint(0, 100), random.randint(0, 100)
    return _task(f"x + {a} = {x + a}", x)


def x_minus_a():  # x - a = b
    a, b = random.randint(0, 100), random.randint(0, 100)
    return _task(f"x - {a} = {b}", a + b)


def a_plus_x():  # a + x = c
    x, a = random.randint(0, 100), random.randint(0, 100)
    return _task(f"{a} + x = {x + a}", x)


def a_minus_x():  # (x + b) - x = b
    x, b = random.randint(0, 100), random.randint(0, 100)
    return _task(f"{x + b} - x = {b}", x)


def x_plus_a_minus_b():  # x + a - b = c
    a = random.randint(0, 100)
    b = random.randint(0, a)
    x = random.randint(0, 100)
    return _task(f"x + {a} - {b} = {x + a - b}", x)


def x_minus_a_plus_b():  # x - a + b = c
    x = random.randint(0, 100)
    a = random.randint(0, x)
    b = random.randint(0, 100)
    return _task(f"x - {a} + {b} = {x - a + b}", x)


def a_plus_x_plus_b():  # a + x + b = c
    x, a, b = (random.randint(0, 100) for _ in range(3))
    return _task(f"{a} + x + {b} = {x + a + b}", x)


def a_plus_x_minus_b():  # a + x - b = c
    x = random.randint(0, 100)
    a = random.randint(0, 100)
    b = random.randint(0, x)
    return _task(f"{a} + x - {b} = {x + a - b}", x)


ADD_SUB = [
    x_plus_a,
    x_minus_a,
    a_plus_x,
    a_minus_x,
    x_plus_a_minus_b,
    x_minus_a_plus_b,
    a_plus_x_plus_b,
    a_plus_x_minus_b,
]


def equations_add_sub():
    """Генератор уравнений сложения и вычитания"""
    return random.choice(ADD_SUB)()


# умножение / деление


def a_times_x():  # a × x = c
    a, x = random.randint(1, 50), random.randint(0, 20)
    return _task(f"{a} × x = {a * x}", x)


def x_times_a():  # x × a = c
    a, x = random.randint(1, 50), random.randint(0, 20)
    return _task(f"x × {a} = {a * x}", x)


def x_div_a():  # x ÷ a = b
    a = random.randint(1, 50)
    b = random.randint(0, a)
    return _task(f"x ÷ {a} = {b}", a * b)


def a_div_x():  # c ÷ x = b
    x = random.randint(1, 50)
    b = random.randint(1, x)
    return _task(f"{x * b} ÷ x = {b}", x)


MUL_DIV = [a_times_x, x_times_a, x_div_a, a_div_x]


def equations_mul_div():
    """Генерирует уравнения на умножение/деление"""
    return random.choice(MUL_DIV)()


# смешанные


def x_times_m_plus_k():
    m, x, k = random.randint(2, 20), random.randint(0, 50), random.randint(0, 100)
    return _task(f"x × {m} + {k} = {x * m + k}", x)


def x_times_m_minus_k():
    m, x = random.randint(2, 20), random.randint(0, 50)
    k = random.randint(0, x * m)
    return _task(f"x × {m} - {k} = {x * m - k}", x)


def equations_mix():
    """Уравнения в два действия (× и +/-)"""
    return random.choice([x_times_m_plus_k, x_times_m_minus_k])()


def equations_all():
    """Объединение всех типов уравнений"""
    return random.choice([equations_add_sub, equations_mul_div, equations_mix])()
