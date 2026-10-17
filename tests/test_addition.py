from unittest.mock import patch

from src.addition import addition_generators
from src.core.task import Task


def test_addition_random():
    with patch("src.addition.random.randint", side_effect=[15, 3]):
        assert addition_generators(20) == Task(text="3 + 12 = ?", answer=15)
