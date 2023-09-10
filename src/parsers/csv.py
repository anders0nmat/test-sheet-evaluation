from interfaces import AnswerParser 
import csv

class CsvParser(AnswerParser):
    # TODO
    def readCSV(csv_path, num_answers):
        Nerd = Student()
        Nerd.id = 0
        result = []
        with open(csv_path, 'r') as csv_file:
            # use CSV reader (all lines)
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for line in csv_reader:
                # extract values
                #question_number = int(line['Question Number'])
                input = line['Correct Answer']
                letter = input.upper()
                if 'A' <= letter <= 'Z':
                    pos_answer = ord(letter) - ord('A')

                    string = num_answers*'O'
                    string = string[:pos_answer] + 'X' + string[pos_answer+1:]
                    result.append(string)

        Nerd.answers = result
        # print(Nerd.answers)
        return Nerd

AnswerParser.register(CsvParser)
