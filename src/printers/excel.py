from src.interfaces import FilePrinter
from openpyxl import Workbook

class ExcelPrinter(FilePrinter):
    def printStatistics(self):
        workbook = Workbook()
        for sheet in self.statBook.sheets:
            worksheet = workbook.create_sheet(title=sheet.name)
            for row in sheet.rows:
                worksheet.append(row.values)
        
        workbook.remove(workbook.active)    
        workbook.save(self.filePath)        

FilePrinter.register(ExcelPrinter)