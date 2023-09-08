
from interfaces import FilePrinter
import printers.csv
import printers.excel

from pathlib import Path
from containers import StatisticsBook
from typing import Optional

def get_printer(path: Path, book: StatisticsBook) -> Optional[FilePrinter]:
    return FilePrinter.getPrinter(path, book=book)
