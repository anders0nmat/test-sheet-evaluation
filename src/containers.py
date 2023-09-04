from dataclasses import dataclass, field

@dataclass
class Answer:
    options: str = ""
    """
    Each char represents one detected answer.
    The char represents the state as well as the certainty

	X : Answer selected
    x : Answer probably selected
    O : Answer empty
    o : Answer probably empty
    # : Unable to detect reliably
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

