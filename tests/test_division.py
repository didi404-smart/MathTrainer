from unittest.mock import patch

from src.MathTrainer.core.task import Task
from src.MathTrainer.generators.division import (
    division_one_digit,
    division_two_digit,
    division_three_digit,
    division_all,
    division_table_10_10
)

PATCH_PATH = "src.MathTrainer.generators.division.random.randint"

def test_division_table_10_10():
    with patch(PATCH_PATH, side_effect=[10, 10]):
        assert division_table_10_10() == Task(
            text="Выполни деление без остатка: 100 ÷ 10 = ?",
            answer=10
        )

def test_division_one_digit():
    with patch(PATCH_PATH, side_effect=[100, 7]):
        assert division_one_digit() == Task(
            text="Выполни деление без остатка: 700 ÷ 7 = ?",
            answer=100,
        )


def test_division_two_digit():
    with patch(PATCH_PATH, side_effect=[100, 10]):
        assert division_two_digit() == Task(
            text="Выполни деление без остатка: 1000 ÷ 10 = ?",
            answer=100,
        )


def test_division_three_digit():
    with patch(PATCH_PATH, side_effect=[100, 100]):
        assert division_three_digit() == Task(
            text="Выполни деление без остатка: 10000 ÷ 100 = ?",
            answer=100,
        )


def test_division_all():
    with patch(PATCH_PATH, side_effect=[100, 999]):
        assert division_all() == Task(
            text="Выполни деление без остатка: 99900 ÷ 999 = ?",
            answer=100
        )