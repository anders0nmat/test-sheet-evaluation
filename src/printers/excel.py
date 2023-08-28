from src.interfaces import FilePrinter

class ExcelPrinter(FilePrinter):
    pass # TODO use openpyxl

FilePrinter.register(ExcelPrinter)
