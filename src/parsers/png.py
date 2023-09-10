from interfaces import AnswerParser
from containers import Student, Answer

class PngParser(AnswerParser):
	def __init__(self, args: list[str]) -> None:
		print(f"Received file: {args[0]}")
		super().__init__()

	def extractAnswers(self) -> list[Student]:
		return [
			Student(id=0, answers=[
				Answer("OXOO"),
				Answer("ooxx"),
				Answer("#oXO"),
			])
		]

AnswerParser.register(PngParser)
