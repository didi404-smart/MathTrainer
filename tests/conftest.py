from unittest.mock import patch

import pytest

MODULE = "src.MathTrainer.generators.equations"


@pytest.fixture
def randint():
    """Подменяет random.randint"""
    with patch(f"{MODULE}.random.randint") as mock:
        yield mock


@pytest.fixture
def choice():
    """Подменяет random.choice."""
    with patch(f"{MODULE}.random.choice") as mock:
        yield mock
