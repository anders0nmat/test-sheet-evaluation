from analysis.sql import SqlAnalyzer
from parsers import get_parser_result
from printers import get_printer
from containers import Student
from pathlib import Path
from typing import Optional

from argparse import ArgumentParser

def getStudents(file: Path, answer_count: int) -> list[Student]:
	file = Path(file)
	return get_parser_result([file, str(answer_count)])

def main():
	print("Running...")
	
	argparser = ArgumentParser(
		prog="src",
		description="Analyze exam sheets"
	)
	argparser.add_argument('sheets', type=Path, help="The sheets to analyze")
	argparser.add_argument('-s', '--solution', type=Path, default=None, help="Solutions for use in analysis")
	argparser.add_argument('-sid', '--solution-id', type=int, default=0, help="The id for the solution sheet 'student' (Default: 0)")
	argparser.add_argument('-o', '--output', type=Path, required=True, help="The path/file where the analysis will be outputted")
	argparser.add_argument('-q', '--sql', type=Path, default=Path('./'), help="File or directory of sql queries (Default: ./)")
	argparser.add_argument('-c', '--count', type=int, default=4, help="Amount of possible answers per question (Default: 4)")
	args = argparser.parse_args()
	# STEP 1 : Get locations

	sheetsPath = args.sheets
	solutionPath = args.solution
	outputPath = args.output

	# STEP 2 : Read sheets & solutions

	students = getStudents(sheetsPath, args.count)

	# Has all answers correct, what a nerd!
	nerd: Optional[Student]
	if solutionPath is not None:
		nerd = getStudents(solutionPath, args.count)
		if len(nerd) > 1:
			raise ValueError() # TODO proper error handling
		nerd = nerd[0] if len(nerd) > 0 else None
		if nerd is not None:
			nerd.id = args.solution_id
	else:
		nerd = None

	# STEP 3 : Analyze...

	statistics = SqlAnalyzer(students, nerd=nerd, sql_path=args.sql)
	book = statistics.analyze()

	# STEP 4 : Print results

	printer = get_printer(outputPath, book=book)
	printer.printStatistics()

	print("Finished!")


if __name__ == "__main__":
	main()
