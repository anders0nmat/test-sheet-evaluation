from .interfaces import AnswerParser, AnswerStatistics, FilePrinter
from .containers import Student
from pathlib import Path

def getStudents(file: Path) -> list[Student]:
    file = Path(file)
    if parser := AnswerParser.getParser(args=[file]):
        return parser.extractAnswers()
    else:
        raise ValueError()

def main():
    print("Running...")

    # STEP 1 : Get locations

    sheetsPath = "" # TODO get sheets from user
    solutionPath = "" # TODO get solution from user
    outputPath = "" # TODO get output path from user

    # STEP 2 : Read sheets & solutions

    students = getStudents(sheetsPath)

    # Has all answers correct, what a nerd!
    nerd = getStudents(solutionPath)
    if len(nerd) > 1:
        raise ValueError() # TODO proper error handling
    nerd = nerd[0] if len(nerd) > 0 else None

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
