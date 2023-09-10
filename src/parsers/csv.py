from interfaces import AnswerParser 
from containers import Student, Answer
from pathlib import Path
import csv

class CsvParser(AnswerParser):
    csvFile: Path
    num_answers: int
    def __init__(self, args: list[str]) -> None:
        super().__init__()
        self.csvFile = Path(args[0])
        self.num_answers = int(args[1])
    
    # TODO
    def readCSV(self, csv_path, num_answers):
        Nerd = Student()
        Nerd.id = 0
        result = [Answer]
        with open(csv_path, 'r') as csv_file:
            # use CSV reader (all lines)
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for line in csv_reader:
                # extract values
                #question_number = int(line['Question Number'])
                input = line['Correct Answer']
                letter = input.upper()
                if 'A' <= letter <= 'Z':
                    answer = Answer()

                    string = num_answers*'O'
                    pos_answer = ord(letter) - ord('A')
                    string = string[:pos_answer] + 'X' + string[pos_answer+1:]

                    answer.options = string
                    result.append(answer)

        Nerd.answers = result
        # print(Nerd.answers)
        return Nerd
    
    def extractAnswers(self) -> list[Student]:
        result = [Student]
        Nerd = Student()
        Nerd = self.readCSV(self.csvFile, self.num_answers)
        result.append(Nerd)
        return result

AnswerParser.register(CsvParser)
