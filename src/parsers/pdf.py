from src.interfaces import AnswerParser

class PdfParser(AnswerParser):
    pass # TODO maybe convert to png and hand off to PngParser

AnswerParser.register(PdfParser)
