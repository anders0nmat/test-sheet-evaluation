from src.containers import StatisticsBook, Student
from src.interfaces import AnswerStatistics
from typing import Optional

import sqlite3

example_sql = """
SELECT *
FROM students
WHERE
question1 LIKE 'X';
"""


class SqlAnalyzer(AnswerStatistics):
	# TODO : More inputs required?
	def __init__(self, students: list[Student], nerd: Optional[Student]) -> None:
		super().__init__(students=students, nerd=nerd)

	def analyze(self) -> StatisticsBook:
		# TODO : implement functionality
		pass



# ==================================
from src.containers import Answer

def test():
	students = [
		Student(1, answers=[
			Answer('XOOO'),
			Answer('OOXO'),
			Answer('OXOx'),
			Answer('oOO#'),
			Answer('X#oX'),
		]),
		Student(2, answers=[
			Answer('xXOO'),
			Answer('OOxO'),
			Answer('OXO#'),
			Answer('OOXO'),
			Answer('X#oX'),
		]),
		Student(3, answers=[
			Answer('XO#O'),
			Answer('OOOO'),
			Answer('xOOO'),
			Answer('xOOO'),
			Answer('####'),
		]),
	]

	nerd = Student(0, answers=[
		Answer('XOOO'),
		Answer('OOXO'),
		Answer('OXOX'),
		Answer('OXOO'),
		Answer('XXOX'),	
	])

	analyzer = SqlAnalyzer(students, nerd=nerd)
	book = analyzer.analyze()

	for idx, sheet in enumerate(book.sheets):
		print(f'Sheet{idx + 1}: {sheet.name}') # Index starts with 0
		for row in sheet.rows:
			row_str = ' | '.join(row.values)
			print(f'\t{row_str}')


if __name__ == "__main__":
	test()
	
