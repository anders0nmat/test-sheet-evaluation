from dataclasses import dataclass, field

@dataclass
class Answer:
    options: list[int] = field(default_factory=lambda:[])
    """
    Each entry represents one detected answer.
    The integer represents a certainty for a specific value:

    -100 : square was empty
       0 : square was crossed
     100 : square was filled
    """

@dataclass
class Student:
    id: int
    answers: list[Answer] = field(default_factory=lambda:[])

@dataclass
class StatisticsRow:
    values: list[str] = field(default_factory=lambda:[])

@dataclass
class StatisticsSheet:
    name: str
    rows: list[StatisticsRow] = field(default_factory=lambda:[])

@dataclass
class StatisticsBook:
    sheets: list[StatisticsSheet] = field(default_factory=lambda:[])

