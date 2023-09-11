from interfaces import AnswerParser
from containers import Student
from pathlib import Path
import tempfile
from parsers.png import PngParser


from pdf2image import convert_from_path

# (sudo apt install python3-pip) falls pip nicht installiert 
# pip install PyPDF2 pdf2image
# sudo apt-get install poppler-utils

class PdfParser(AnswerParser):
	EXTENSIONS = {'.pdf'}

	pdfFile: Path
	def __init__(self, args: list[str]) -> None:
		super().__init__()
		self.pdfFile = Path(args[0])

	def pdf_to_png(self, pdf_file, output_folder) -> list[Path]:
		# Seiten des PDFs in PNG-Bilder konvertieren
		images: list[Path] = convert_from_path(pdf_file,
			dpi=200,
			output_folder=output_folder,
			paths_only=True,
			fmt="png")

		#for i, image in enumerate(images):
		#    image.save(f"{output_folder}/{i + 1}.png", "PNG")
		
		return images
	
	def extractAnswers(self) -> list[Student]:
		with tempfile.TemporaryDirectory() as temp_directory:
			png_paths = self.pdf_to_png(self.pdfFile, temp_directory)

			result: list[Student] = []

			for idx, path in enumerate(png_paths):
				#png_file :Path
				#png_file = f"{temp_directory}/{i + 1}.png"
				parser = PngParser(args=[path])
				[ student ] = parser.extractAnswers()
				student.id = idx + 1
				result.append(student)

		return result

AnswerParser.register(PdfParser)
