from src.interfaces import AnswerParser
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

# (sudo apt install python3-pip) falls pip nicht installiert 
# pip install PyPDF2 pdf2image
# sudo apt-get install poppler-utils

class PdfParser(AnswerParser):
    # TODO maybe convert to png and hand off to PngParser
    def pdf_to_png(pdf_file, output_folder):
        # PDF-Datei öffnen und deren Seitenanzahl erhalten
        pdf = PdfReader(open(pdf_file, 'rb'))
        num_pages = len(pdf.pages)

        # Seiten des PDFs in PNG-Bilder konvertieren
        for page_num in range(num_pages):
            images = convert_from_path(pdf_file, dpi=200, first_page=page_num + 1, last_page=page_num + 1)

            for i, image in enumerate(images):
                image.save(f"{output_folder}/page_{page_num + 1}_{i + 1}.png", "PNG")

AnswerParser.register(PdfParser)
