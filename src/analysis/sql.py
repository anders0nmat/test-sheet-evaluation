from containers import StatisticsBook, StatisticsSheet, StatisticsRow, Student
from interfaces import AnswerStatistics
from typing import Optional
from pathlib import Path

import sqlite3

example_sql = """
SELECT id, question, box1 as A
FROM students
WHERE
question1 LIKE question1(WHERE name = "nerd");
"""


class SqlAnalyzer(AnswerStatistics):
	def __init__(self, students: list[Student], nerd: Optional[Student], sql_path: Path) -> None:
		super().__init__(students=students, nerd=nerd)
		self.sql_path = Path(sql_path)
		# count checkboxes:
		if self.nerd is not None:
			self.box_count = len(self.nerd.answers[0].options)
		else:
			self.box_count = len(self.students[0].answers[0].options) 
		# print("Total number of boxes:", self.box_count)
	
	def analyze(self) -> StatisticsBook:
		with self.create_connection() as conn:		# does the same as: conn = self.create_connection()

			if conn is not None:
				self.create_table(conn)
				self.insert_data(conn)
				# self.check_tables(conn)
				return self.execute_sql(conn)
			else: 
				raise ValueError("404 connection not found")

	

	def create_connection(self):
		conn = sqlite3.connect(':memory:')
		return conn


	def create_table(self, conn: sqlite3.Connection):
		#count number of questions

		boxes = " "
		for i in range(self.box_count): 
			boxes += ", box" + str(i)
		# print(boxes)

		cur = conn.cursor()
		cur.execute(f"CREATE TABLE IF NOT EXISTS results(id int, question int{boxes})")

	
	def insert_data(self, conn: sqlite3.Connection):
		cur = conn.cursor()
		
		sql_data = []

		if self.nerd is not None:
			student = self.nerd
			for iq, question in enumerate(student.answers):
				sql_params = [
					student.id,
					iq+1,
				]
				for checkbox in question.options:
					sql_params.append(checkbox)

				sql_data.append(sql_params)

		for student in self.students:
			for iq, question in enumerate(student.answers):
				sql_params = [
					student.id,
					iq+1,
				]
				for checkbox in question.options:
					sql_params.append(checkbox)

				sql_data.append(sql_params)
		
		boxes = ["?"] * self.box_count
		boxes = ", ".join(boxes)


		cur.executemany(f"INSERT INTO results VALUES (?, ?, {boxes})", sql_data)


# Checks are to be done in here
#	def check_tables(self, conn: sqlite3.Connection):
#		cur = conn.cursor()
#		cur.execute("SELECT *  FROM results")
#		res = [entry for entry in cur.fetchall()]
#		print("data:", res)
#		cur.execute("SELECT name  FROM sqlite_master")
#		res = [entry[0] for entry in cur.fetchall()]
#		print("established tables:", res)




	def get_sql_files(self) -> list[Path]:
		if self.sql_path.is_file():
			return [self.sql_path]
		elif self.sql_path.is_dir():
			all_files = self.sql_path.glob('**/*.sql') # gets everything with name = *.sql
			all_files = [path for path in all_files if path.is_file()] # filters for files
			return all_files
		else:
			raise ValueError("Unknown Path type")



	def execute_sql(self, conn: sqlite3.Connection)->StatisticsBook:
		cur = conn.cursor()
		book = StatisticsBook()

		for file in self.get_sql_files():
			query = file.read_text()
			sheet = StatisticsSheet(file.stem)
			cur.execute(query)
			sheet.rows.append(StatisticsRow([col_data[0] for col_data in cur.description]))
			for row in cur.fetchall():
				str_row = [str(value) for value in row]
				sheet.rows.append(StatisticsRow(str_row))
			book.sheets.append(sheet)

		return book



# =========================================================
from containers import Answer

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

	analyzer = SqlAnalyzer(students, nerd=nerd, sql_path=r"./sql_queries")
	book = analyzer.analyze()

	for idx, sheet in enumerate(book.sheets):
		print(f'Sheet{idx + 1}: {sheet.name}') # Index starts with 0
		for row in sheet.rows:
			row_str = ' | '.join(row.values)
			print(f'\t{row_str}')


if __name__ == "__main__":
	test()
	
