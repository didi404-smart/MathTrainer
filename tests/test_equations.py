from unittest.mock import Mock

import pytest

from src.MathTrainer.generators import equations as eq

# генератор, что вернёт randint по порядку вызовов, текст, ответ
CASES = [
    # сложение / вычитание
    (eq.x_plus_a, [5, 3], "x + 3 = 8", 5),  # x=5, a=3
    (eq.x_minus_a, [10, 4], "x - 10 = 4", 14),  # a=10, b=4
    (eq.a_plus_x, [5, 3], "3 + x = 8", 5),  # x=5, a=3
    (eq.a_minus_x, [5, 3], "8 - x = 3", 5),  # x=5, b=3
    (eq.x_plus_a_minus_b, [10, 4, 5], "x + 10 - 4 = 11", 5),  # a=10, b=4, x=5
    (eq.x_minus_a_plus_b, [10, 4, 3], "x - 4 + 3 = 9", 10),  # x=10, a=4, b=3
    (eq.a_plus_x_plus_b, [5, 2, 3], "2 + x + 3 = 10", 5),  # x=5, a=2, b=3
    (eq.a_plus_x_minus_b, [5, 2, 3], "2 + x - 3 = 4", 5),  # x=5, a=2, b=3
    # умножение / деление
    (eq.a_times_x, [4, 3], "4 × x = 12", 3),  # a=4, x=3
    (eq.x_times_a, [4, 3], "x × 4 = 12", 3),  # a=4, x=3
    (eq.x_div_a, [5, 2], "x ÷ 5 = 2", 10),  # a=5, b=2
    (eq.a_div_x, [6, 2], "12 ÷ x = 2", 6),  # x=6, b=2
    # смешанные
    (eq.x_times_m_plus_k, [3, 4, 5], "x × 3 + 5 = 17", 4),  # m=3, x=4, k=5
    (eq.x_times_m_minus_k, [3, 4, 5], "x × 3 - 5 = 7", 4),  # m=3, x=4, k=5
]


@pytest.mark.parametrize("generator, numbers, text, answer", CASES, ids=[c[0].__name__ for c in CASES])
def test_generator(randint, generator, numbers, text, answer):
    randint.side_effect = numbers

    task = generator()

    assert task.text == f"{eq.PREFIX}{text}"
    assert task.answer == answer


def test_add_sub_picks_from_add_sub_list(choice):
    choice.return_value = Mock(return_value="task")

    assert eq.equations_add_sub() == "task"
    choice.assert_called_once_with(eq.ADD_SUB)


def test_mul_div_picks_from_mul_div_list(choice):
    choice.return_value = Mock(return_value="task")

    assert eq.equations_mul_div() == "task"
    choice.assert_called_once_with(eq.MUL_DIV)


def test_mix_picks_from_mix_patterns(choice):
    choice.return_value = Mock(return_value="task")

    assert eq.equations_mix() == "task"
    choice.assert_called_once_with([eq.x_times_m_plus_k, eq.x_times_m_minus_k])


def test_all_picks_from_all_groups(choice):
    choice.return_value = Mock(return_value="task")

    assert eq.equations_all() == "task"
    choice.assert_called_once_with([eq.equations_add_sub, eq.equations_mul_div, eq.equations_mix])
