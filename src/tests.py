
from parsers.csv import CsvParser

parser = CsvParser(['./test_data.csv'])
result = parser.extractAnswers()
print(result)
