import csv
from interfaces import FilePrinter

class CsvPrinter(FilePrinter):
	EXTENSIONS = {'.csv'}

	def printStatistics(self):
		for sheet in self.statBook.sheets:
			sheet_name = sheet.name
			sheet_data = sheet.rows
			sheet_filename = f"{self.filePath.stem}_{sheet_name}.csv"

			with open(self.filePath.with_name(sheet_filename), 'w', newline='', encoding='utf-8') as csvfile:
				csv_writer = csv.writer(csvfile, delimiter=',')
				for row in sheet_data:
					csv_writer.writerow(row.values)

FilePrinter.register(CsvPrinter)