from dataclasses import dataclass, field

@dataclass
class Answer:
	options: str = ""
	"""
	Each char represents one detected answer.
	The char represents the state as well as the certainty

	- 'X' : Answer selected  
	- 'x' : Answer probably selected  
	- 'O' : Answer empty  
	- 'o' : Answer probably empty  
	- '#' : Unable to detect reliably
	"""
	
	def has_missing(self) -> bool:
		return '#' in self.options

@dataclass
class Student:
	id: int
	answers: list[Answer] = field(default_factory=lambda:[])

	def has_missing(self) -> bool:
		return any(a.has_missing() for a in self.answers)

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

