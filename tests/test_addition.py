from unittest.mock import patch

from src.MathTrainer.core.task import Task
from src.MathTrainer.generators.addition import addition_generators


def test_addition_random():
    with patch("src.MathTrainer.generators.addition.random.randint", side_effect=[15, 3]):
        assert addition_generators(20) == Task(text="3 + 12 = ?", answer=15)
