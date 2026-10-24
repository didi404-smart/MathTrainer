from unittest.mock import patch

from src.MathTrainer.core.task import Task
from src.MathTrainer.generators.multiplication import (
    multiplication_all,
    multiplication_four_digit,
    multiplication_one_digit,
    multiplication_table_10_10,
    multiplication_three_digit,
    multiplication_two_digit,
)


def test_multiplication_table_10_10():
    with patch("src.MathTrainer.generators.multiplication.random.randint", side_effect=[8, 9]):
        assert multiplication_table_10_10() == Task(text="Выполни умножение 8 × 9 = ?", answer=72)


def test_multiplication_one_digit():
    with patch("src.MathTrainer.generators.multiplication.random.randint", side_effect=[100, 9]):
        assert multiplication_one_digit() == Task(text="Выполни умножение(столбиком) 100 × 9 = ?", answer=900)


def test_multiplication_two_digit():
    with patch("src.MathTrainer.generators.multiplication.random.randint", side_effect=[100, 10]):
        assert multiplication_two_digit() == Task(text="Выполни умножение(столбиком) 100 × 10 = ?", answer=1000)


def test_multiplication_three_digit():
    with patch("src.MathTrainer.generators.multiplication.random.randint", side_effect=[100, 100]):
        assert multiplication_three_digit() == Task(text="Выполни умножение(столбиком) 100 × 100 = ?", answer=10000)


def test_multiplication_four_digit():
    with patch("src.MathTrainer.generators.multiplication.random.randint", side_effect=[1000, 1000]):
        assert multiplication_four_digit() == Task(text="Выполни умножение(столбиком) 1000 × 1000 = ?", answer=1000000)


def test_multiplication_all():
    with patch("src.MathTrainer.generators.multiplication.random.randint", side_effect=[10, 100]):
        assert multiplication_all() == Task(text="Выполни умножение(столбиком) 10 × 100 = ?", answer=1000)
