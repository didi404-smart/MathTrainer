from src.MathTrainer.core.task import Task
from src.MathTrainer.generators.division import (
    division_all,
    division_one_digit,
    division_table_10_10,
    division_three_digit,
    division_two_digit,
)

PREFIX = "Выполни деление без остатка: "


def test_division_table_10_10(randint):
    randint.side_effect = [10, 10]

    assert division_table_10_10() == Task(text=f"{PREFIX}100 ÷ 10 = ?", answer=10)


def test_division_one_digit(randint):
    randint.side_effect = [100, 7]

    assert division_one_digit() == Task(text=f"{PREFIX}700 ÷ 7 = ?", answer=100)


def test_division_two_digit(randint):
    randint.side_effect = [100, 10]

    assert division_two_digit() == Task(text=f"{PREFIX}1000 ÷ 10 = ?", answer=100)


def test_division_three_digit(randint):
    randint.side_effect = [100, 100]

    assert division_three_digit() == Task(text=f"{PREFIX}10000 ÷ 100 = ?", answer=100)


def test_division_all(randint):
    randint.side_effect = [100, 999]

    assert division_all() == Task(text=f"{PREFIX}99900 ÷ 999 = ?", answer=100)
