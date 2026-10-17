from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    text: str
    answer: int
