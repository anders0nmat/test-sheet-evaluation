import abc
from containers import Student, StatisticsBook
from pathlib import Path
from typing import Optional, Any, Type

class AnswerParser:
	__parsers__: list[Type["AnswerParser"]] = []

	@staticmethod
	def register(parser: Type["AnswerParser"]):
		AnswerParser.__parsers__.append(parser)

	@staticmethod
	def getParser(args: list[Any]) -> Optional["AnswerParser"]:
		for parserClass in AnswerParser.__parsers__:
			if parserClass.canParse(args):
				return parserClass(args)
		return None
	
	@abc.abstractmethod
	def extractAnswers(self) -> list[Student]:
		pass

	@abc.abstractclassmethod
	def canParse(cls, args: list[Any]) -> bool:
		pass

class AnswerStatistics:
	students: list[Student]
	nerd: Optional[Student]

	def init(self, students: list[Student], nerd: Optional[Student]):
		self.students = students
		self.nerd = nerd

	@abc.abstractmethod
	def analyze(self) -> StatisticsBook:
		pass



class StatisticsPrinter:
	statBook: StatisticsBook

	def __init__(self, statBook: StatisticsBook) -> None:
		self.statBook = statBook

	@abc.abstractmethod
	def printStatistics(self):
		pass

class FilePrinter(StatisticsPrinter):
	__printers__: list[Type["FilePrinter"]] = []
	
	EXTENSIONS: set[str] = set()

	filePath: Path

	def __init__(self, statBook: StatisticsBook, path: Path):
		super().__init__(statBook)
		self.filePath = Path(path)

	@staticmethod
	def register(parser: Type["FilePrinter"]):
		FilePrinter.__printers__.append(parser)

	@staticmethod
	def getPrinter(path: Any, book: StatisticsBook) -> Optional["FilePrinter"]:
		for printerClass in FilePrinter.__printers__:
			if printerClass.canPrint(path=Path(path), book=book):
				return printerClass(book, path=Path(path))
		return None
	
	@classmethod
	def canPrint(cls, path: Path, book: StatisticsBook) -> bool:
		return path.suffix.casefold() in {e.casefold() for e in cls.EXTENSIONS}
	


