
from interfaces import AnswerParser
import parsers.csv
import parsers.pdf
import parsers.png

from typing import Optional
from containers import Student

def get_parser(args: list[str]) -> Optional[AnswerParser]:
    return AnswerParser.getParser(args=args)

def get_parser_result(args: list[str]) -> Optional[list[Student]]:
	if parser := get_parser(args=args):
		return parser.extractAnswers()
	else:
		return None

