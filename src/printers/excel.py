from src.interfaces import FilePrinter
from openpyxl import Workbook
from pathlib import Path

class ExcelPrinter(FilePrinter):
	def printStatistics(self):
		workbook = Workbook()
		for sheet in self.statBook.sheets:
			worksheet = workbook.create_sheet(title=sheet.name)
			for row in sheet.rows:
				worksheet.append(row.values)
		
		workbook.remove(workbook.active)    
		workbook.save(self.filePath)

	@classmethod
	def canPrint(cls, path: Path, book) -> bool:
		return path.suffix.casefold() in {'.xlsx', '.xls'}

FilePrinter.register(ExcelPrinter)