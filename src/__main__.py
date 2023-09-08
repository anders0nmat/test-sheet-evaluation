from interfaces import AnswerParser, AnswerStatistics, FilePrinter
from containers import Student
from pathlib import Path

from argparse import ArgumentParser

def getStudents(file: Path) -> list[Student]:
	file = Path(file)
	if parser := AnswerParser.getParser(args=[file]):
		return parser.extractAnswers()
	else:
		raise ValueError()

def main():
	print("Running...")
	
	argparser = ArgumentParser(
		prog="src",
		description="Analyze exam sheets"
	)
	argparser.add_argument('sheets', type=Path, help="The sheets to analyze")
	argparser.add_argument('-s', '--solution', type=Path, help="Solutions for use in analysis")
	argparser.add_argument('-sid', '--solution-id', type=int, default=0, help="The id for the solution sheet 'student' (Default: 0)")
	argparser.add_argument('-o', '--output', required=True, type=Path, help="The path/file where the analysis will be outputted")
	args = argparser.parse_args()
	# STEP 1 : Get locations

	sheetsPath = args.sheets
	solutionPath = args.solution
	outputPath = args.output

	# STEP 2 : Read sheets & solutions

	students = getStudents(sheetsPath)

	# Has all answers correct, what a nerd!
	nerd = getStudents(solutionPath)
	if len(nerd) > 1:
		raise ValueError() # TODO proper error handling
	nerd = nerd[0] if len(nerd) > 0 else None
	if nerd is not None:
		nerd.id = args.solution_id

	# STEP 3 : Analyze...

	# TODO build proper statistics class
	statistics = AnswerStatistics(students, nerd=nerd)
	book = statistics.analyze()

	# STEP 4 : Print results

	printer = FilePrinter.getPrinter(outputPath, book=book)
	printer.printStatistics()

	print("Finished!")


if __name__ == "__main__":
	main()
