from unittest.mock import Mock, call

import pytest

from src.MathTrainer.generators import equations as eq

LIMIT = 100

# (генератор, что вернёт randint по порядку вызовов, текст, ответ)
CASES = [
    # сложение / вычитание
    (eq.x_plus_a,          [5, 3],     "x + 3 = 8",      5),    # x=5, a=3
    (eq.x_minus_a,         [10, 4],    "x - 4 = 6",      10),   # x=10, a=4
    (eq.a_plus_x,          [5, 3],     "3 + x = 8",      5),    # x=5, a=3
    (eq.a_minus_x,         [10, 4],    "10 - x = 6",     4),    # a=10, x=4
    (eq.x_plus_a_minus_b,  [5, 3, 2],  "x + 3 - 2 = 6",  5),    # x=5, a=3, b=2
    (eq.x_minus_a_plus_b,  [10, 4, 3], "x - 4 + 3 = 9",  10),   # x=10, a=4, b=3
    (eq.a_plus_x_plus_b,   [5, 2, 3],  "2 + x + 3 = 10", 5),    # x=5, a=2, b=3
    (eq.a_plus_x_minus_b,  [5, 2, 3],  "2 + x - 3 = 4",  5),    # x=5, a=2, b=3
    # умножение / деление
    (eq.a_times_x,         [4, 3],     "4 × x = 12",     3),    # a=4, x=3
    (eq.x_times_a,         [4, 3],     "x × 4 = 12",     3),    # a=4, x=3
    (eq.x_div_a,           [5, 2],     "x ÷ 5 = 2",      10),   # a=5, b=2
    (eq.a_div_x,           [6, 2],     "12 ÷ x = 2",     6),    # x=6, b=2
    # смешанные
    (eq.x_times_m_plus_k,  [3, 4, 5],  "x × 3 + 5 = 17", 4),    # m=3, x=4, k=5
    (eq.x_times_m_minus_k, [3, 4, 5],  "x × 3 - 5 = 7",  4),    # m=3, x=4, k=5
]


@pytest.mark.parametrize("generator, numbers, text, answer", CASES,
                         ids=[c[0].__name__ for c in CASES])
def test_generator(randint, generator, numbers, text, answer):
    randint.side_effect = numbers

    task = generator(LIMIT)

    assert task.text == f"{eq.PREFIX}{text}"
    assert task.answer == answer


def test_x_plus_a_sum_stays_within_limit(randint):
    randint.side_effect = [5, 3]

    eq.x_plus_a(100)

    assert randint.call_args_list == [call(0, 100), call(0, 95)]


def test_a_plus_x_plus_b_sum_stays_within_limit(randint):
    randint.side_effect = [5, 2, 3]

    eq.a_plus_x_plus_b(100)

    assert randint.call_args_list == [call(0, 100), call(0, 95), call(0, 93)]


@pytest.mark.parametrize("limit, side", [(100, 10), (1000, 31)])
def test_factors_limited_by_sqrt_of_limit(randint, limit, side):
    randint.side_effect = [4, 3]

    eq.a_times_x(limit)

    assert randint.call_args_list == [call(1, side), call(0, side)]


def test_a_div_x_result_never_zero(randint):
    randint.side_effect = [6, 2]

    eq.a_div_x(100)

    assert randint.call_args_list == [call(1, 10), call(1, 10)]


PUBLIC = [
    (eq.equations_add_sub, [eq.ADD_SUB]),
    (eq.equations_mul_div, [eq.MUL_DIV]),
    (eq.equations_mix,     [eq.MIX]),
    (eq.equations_all,     [eq.ADD_SUB + eq.MUL_DIV + eq.MIX]),
]


@pytest.mark.parametrize("public, patterns", PUBLIC,
                         ids=[p[0].__name__ for p in PUBLIC])
def test_public_with_limit(choice, public, patterns):
    pattern = Mock(return_value="task")
    choice.return_value = pattern

    assert public(100) == "task"

    choice.assert_called_once_with(patterns[0])  # предел задан, его не выбираем
    pattern.assert_called_once_with(100)


@pytest.mark.parametrize("public, patterns", PUBLIC,
                         ids=[p[0].__name__ for p in PUBLIC])
def test_public_without_limit_picks_random_limit(choice, public, patterns):
    pattern = Mock(return_value="task")
    choice.side_effect = [1000, pattern]  # сначала предел, потом шаблон

    assert public() == "task"

    assert choice.call_args_list == [call(eq.LIMITS), call(patterns[0])]
    pattern.assert_called_once_with(1000)