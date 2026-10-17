from src.MathTrainer.generators.subtraction import subtraction_generators
from unittest.mock import patch
from src.MathTrainer.core.task import Task
def test_subtraction_generators():
    with patch("src.MathTrainer.generators.subtraction.random.randint", side_effect=[15, 3]):
        assert subtraction_generators(20) == Task(text='15 - 3 = ?', answer=12)