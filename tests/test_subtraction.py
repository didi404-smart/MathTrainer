from src.MathTrainer.core.task import Task
from src.MathTrainer.generators.subtraction import subtraction_generators


def test_subtraction_generators(randint):
    randint.side_effect = [15, 3]
    assert subtraction_generators(20) == Task(text="15 - 3 = ?", answer=12)
