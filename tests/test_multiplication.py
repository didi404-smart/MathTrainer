from src.MathTrainer.core.task import Task
from src.MathTrainer.generators.multiplication import (
    multiplication_all,
    multiplication_four_digit,
    multiplication_one_digit,
    multiplication_table_10_10,
    multiplication_three_digit,
    multiplication_two_digit,
)

PREFIX = "Выполни умножение(столбиком) "


def test_multiplication_table_10_10(randint):
    randint.side_effect = [8, 9]

    assert multiplication_table_10_10() == Task(text="Выполни умножение 8 × 9 = ?", answer=72)


def test_multiplication_one_digit(randint):
    randint.side_effect = [100, 9]

    assert multiplication_one_digit() == Task(text=f"{PREFIX}100 × 9 = ?", answer=900)


def test_multiplication_two_digit(randint):
    randint.side_effect = [100, 10]

    assert multiplication_two_digit() == Task(text=f"{PREFIX}100 × 10 = ?", answer=1000)


def test_multiplication_three_digit(randint):
    randint.side_effect = [100, 100]

    assert multiplication_three_digit() == Task(text=f"{PREFIX}100 × 100 = ?", answer=10000)


def test_multiplication_four_digit(randint):
    randint.side_effect = [1000, 1000]

    assert multiplication_four_digit() == Task(text=f"{PREFIX}1000 × 1000 = ?", answer=1_000_000)


def test_multiplication_all(randint):
    randint.side_effect = [10, 100]

    assert multiplication_all() == Task(text=f"{PREFIX}10 × 100 = ?", answer=1000)
