from src.interfaces import AnswerParser
import PyPDF2
from wand.image import Image

class PdfParser(AnswerParser):
   # TODO maybe convert to png and hand off to PngParser

    def pdf_to_png(pdf_file, output_folder):
        # Öffnen der PDF-Datei
        pdf = PyPDF2.PdfFileReader(open(pdf_file, 'rb'))

        # Schleife durch die Seiten der PDF-Datei
        for page_num in range(pdf.numPages):
            # PDF-Seite extrahieren
            pdf_page = pdf.getPage(page_num)

            # PDF-Seite in ein PNG-Bild konvertieren
            with Image(blob=pdf_page.extractText().encode('utf-8'), format='pdf') as img:
                img.save(filename=f"{output_folder}/page_{page_num + 1}.png")

AnswerParser.register(PdfParser)
