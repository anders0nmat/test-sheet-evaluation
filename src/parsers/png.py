from interfaces import AnswerParser
from containers import Student, Answer
from typing import Any, TypeAlias, Callable, TypeVar, Optional
from dataclasses import dataclass

import cv2
import cv2.typing
import numpy
import itertools

cv2Img: TypeAlias = cv2.typing.MatLike
T = TypeVar('T')

@dataclass
class CheckBox:
	x: int
	y: int
	w: int
	h: int
	value: int = -1

	@property
	def top_left(self) -> tuple[int, int]:
		return (self.x, self.y)
	
	@property
	def bottom_right(self) -> tuple[int, int]:
		return (self.x + self.w, self.y + self.h)
	
	def area(self) -> int:
		return self.w * self.h
	
CheckRow: TypeAlias = list[Optional[CheckBox]]

def split_list(list: list[T], predicate: Callable[[T, T], bool]) -> list[list[T]]:
	""" Splits a list based on a predicate between two elements """
	if len(list) < 2:
		return list
	result = []
	start_idx = 0
	for idx, e in enumerate(list):
		if idx == 0: continue # skip first element
		if predicate(list[idx - 1], e):
			# Split here
			result.append(list[start_idx:idx])
			start_idx = idx
	
	result.append(list[start_idx:])
	return result

class PngParser(AnswerParser):
	# Threshold to concider pixels black/white. Values 0 - 255
	BINARY_IMG_THRESHOLD = 180

	# Size to which all images are scaled (helps with later processing steps). Values: (width, heith)
	IMAGE_SIZE = (1240, 1754)
	# Method to scale images to IMGAGE_SIZE
	IMAGE_SCALE_METHOD = cv2.INTER_NEAREST_EXACT

	# Length at which lines are concidered large. Used for detecting answer box region
	# The size should be large enough to just catch frames and ignore/omit answer boxes/text/other small details
	LARGE_LINE_SIZE = 100

	# FRAME RECTANGLES
	
	# Min width in % to be concidered a relevant frame
	RECT_MIN_WIDTH = 0.80

	# Top edge of top rectangle should be between 0% and TOP_RECT_START_Y % of page height
	TOP_RECT_START_Y = 0.25
	# Top rect should be between low% and high% of page height. Values (low, high)
	TOP_RECT_HEIGHT = (0.25, 0.40)

	# Top edge of bottom rectangle should be greater that BOTTOM_RECT_START_Y % of page height
	BOTTOM_RECT_START_Y = 0.75

	# Tolerance of the width/height-ratio to still be cincidered a square. Relevant for detecting answer boxes	
	SQUARE_TOLERANCE = 0.1

	# Tolerance in x coord where boxes are concidered as "in the same column group"
	# Explanation: "column group" refers to the fact that because of the sheer amount of questions,
	# they are layed out next to each other on the page. A "column group" is one column of these questions
	X_TOLERANCE = 100
	# Tolerance in y coord where boxes are concidered as "in the same row"
	Y_TOLERANCE = 10
	# Tolerance where boxes of different rows are concidered as "in the same answer column"
	QUESTION_THRESHOLD = 10

	# Thresholds for box and associated values. Values (low, high, value)
	RATIOS = [
		(0.00, 0.20, '#'),
		(0.20, 0.27, 'o'),
		(0.27, 0.38, 'O'),
		(0.38, 0.43, 'o'),
		(0.43, 0.48, 'x'),
		(0.48, 0.60, 'X'),
		(0.60, 0.65, 'x'),
		(0.65, 0.75, 'o'),
		(0.75, 1.10, 'O'),

		# Catches holes in definition space. >1 because range check is truly less for upper border
		(0.00, 1.10, '#'), 
	]

	# === DEBUG ===
	PREVIEW_WINDOW_SIZE = (600, 800)


	def __init__(self, args: list[str]) -> None:
		# For debug purposes
		# 0 = all, 1 = important, 2 = none
		self.show_priority_threshold = 0

		self.image = cv2.imread(args[0])
		self.image = cv2.resize(self.image, self.IMAGE_SIZE, interpolation=self.IMAGE_SCALE_METHOD)
		
		gray_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		_, img = cv2.threshold(gray_img, self.BINARY_IMG_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
		self.binary_image = img

		self.show_image("Grayscale Image", self.image, priority=0)
		self.show_image("Binary Image", self.binary_image, priority=0)

		self.image, self.binary_image = self.get_answer_box()

	def show_image(self, view_name, image, priority: int=2):
		if priority >= self.show_priority_threshold:
			cv2.namedWindow(view_name, cv2.WINDOW_KEEPRATIO)
			cv2.imshow(view_name, image)
			cv2.resizeWindow(view_name, self.PREVIEW_WINDOW_SIZE[0], self.PREVIEW_WINDOW_SIZE[1])
			cv2.waitKey(0)
			cv2.destroyAllWindows()

	def get_hv_img(self, binary_img: cv2Img, min_line_len: float) -> cv2Img:
		kernel_h = numpy.ones((1, min_line_len), numpy.uint8)
		kernel_v = numpy.ones((min_line_len, 1), numpy.uint8)

		img_h = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel_h)
		img_v = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel_v)
		
		self.show_image("H-Lines", img_h, priority=0)
		self.show_image("V-Lines", img_v, priority=0)

		return img_h | img_v

	def find_answer_box(self) -> CheckBox:
		# Find region of image where answers are located
		# 		
		img = self.get_hv_img(self.binary_image, min_line_len=self.LARGE_LINE_SIZE)
		self.show_image("Big Boxes", img)
		_, _, stats, _ = cv2.connectedComponentsWithStats(img, connectivity=8)

		# We want the rectangle between rectangle A and B
		# A is spanning vertically roughly half the page
		# B is to the end of the page
		# both span >80% of the width of the page

		img_height, img_width = self.image.shape[:2]

		answer_top_y = None
		answer_bottom_y = None

		out_img = self.image.copy()

		for x, y, w, h, _area in stats[1:]:
			if w > self.RECT_MIN_WIDTH * img_width:
				if answer_top_y is None and y < self.TOP_RECT_START_Y * img_height and self.TOP_RECT_HEIGHT[0] <= h / img_height <= self.TOP_RECT_HEIGHT[1]:
					answer_top_y = y + h
				elif answer_bottom_y is None and y > self.BOTTOM_RECT_START_Y * img_height:
					answer_bottom_y = y

				if self.show_priority_threshold < 1:
					cv2.rectangle(out_img, (x, y), (x+w, y+h), (0, 0, 255), 2)

		self.show_image("Big Boxes", out_img, priority=0)
					

		assert answer_top_y is not None, "Top border not found"
		assert answer_bottom_y is not None, "Bottom border not found"

		return CheckBox(
			x=0,
			y=answer_top_y,
			w=img_width,
			h=answer_bottom_y - answer_top_y
		)

	def get_answer_box(self) -> tuple[cv2Img, cv2Img]:
		answer_box = self.find_answer_box()
		if self.show_priority_threshold < 2:
			img = self.image.copy()
			cv2.rectangle(img, answer_box.top_left, answer_box.bottom_right, (0, 0, 255), 2)
			self.show_image("Answer Box", img)
		
		(x_top, y_top) = answer_box.top_left
		(x_bottom, y_bottom) = answer_box.bottom_right

		cropped_img = self.image[y_top:y_bottom, x_top:x_bottom].copy()
		cropped_binary_img = self.binary_image[y_top:y_bottom, x_top:x_bottom].copy()

		return (cropped_img, cropped_binary_img)
	
	def get_checkboxes(self) -> list[CheckBox]:	

		binary_hv_img = self.get_hv_img(self.binary_image, min_line_len=15)
		self.show_image("Detected Boxes", binary_hv_img, priority=0)
		_, _, stats, _ = cv2.connectedComponentsWithStats(binary_hv_img, connectivity=8)

		checkboxes = []
		for x, y, w, h, _area in stats[1:]:
			ratio = w / h
			if 1 - self.SQUARE_TOLERANCE <= ratio <= 1 + self.SQUARE_TOLERANCE:
				checkboxes.append(CheckBox(x, y, w, h, value=cv2.countNonZero(self.binary_image[y:y+h , x:x+w])))
		
		return checkboxes

	def extractAnswers(self) -> list[Student]:
		# High level order of operations:
		# I. Get Checkboxes
		# II. Sort checkboxes and mark missing ones
		# III. Evaluate checkboxes


		# I. Get Checkboxes
		checkboxes = self.get_checkboxes()


		# II. Sort checkboxes and mark missing ones

		# TODO : Sort checkboxes into groups
		# Idea:
		# 1. Order by x-level
		# 2. Split where significant jump occures
		# 3. Order rows by y-level
		# 4. Split where prev-to-current jump is too high
		# 5. Find if we have missing boxes and insert *None* to indicate so


		# 1. Order by x-level
		checkboxes.sort(key=lambda box: box.x)
		# 2. Split where significant jump occures
		checkbox_columns = split_list(checkboxes, lambda a, b: abs(a.x - b.x) > self.X_TOLERANCE)

		answers: list[CheckRow] = []

		# The amount of answers for a question, used to detect missing boxes
		question_count = None

		for idx, column in enumerate(checkbox_columns):
			# 3. Order rows by y-level
			column.sort(key=lambda box: box.y)
			# 4. Split where prev-to-current jump is too high
			questions = split_list(column, lambda a, b: abs(a.y - b.y) > self.Y_TOLERANCE)
			for q in questions:
				q.sort(key=lambda box: box.x)

			# A question we concider complete (so no missing boxes)
			prototype_question = None

			# Group questions by answer count
			q_count_map: dict[int, list[CheckRow]] = {}
			for question in questions:
				key = len(question)
				if key not in q_count_map:
					q_count_map[key] = []
				q_count_map[key].append(question)

			# Find prototype question
			if question_count is None:
				idx, _ = max(q_count_map.items(), key=lambda item: len(item[1]))
				prototype_question = q_count_map[idx][0]
				question_count = idx
			else:
				if question_count in q_count_map:
					prototype_question = q_count_map[question_count][0]
				else:
					raise ValueError("No complete question in this column")

			# Go through all questions with less than question_count
			# And match boxes with boxes from prototype to find which boxes are missing
			for q_list in [v for k, v in q_count_map.items() if k < question_count]:
				for q in q_list:
					if len(q) == 0:
						q.extend([None] * question_count)
					else:
						possible_mappings = (p for p in itertools.product(q, prototype_question))
						plausible_mappings = (p for p in possible_mappings if abs(p[0].x - p[1].x) < self.QUESTION_THRESHOLD)
						used_prototype_questions = [q for _, q in plausible_mappings]
						# Find indices of proto boxes we weren't able to find a counterpart for
						missing_q_idx = (idx for idx, _ in filter(lambda e: e[1] not in used_prototype_questions, enumerate(prototype_question)))
						# Mark these boxes as missing
						for idx in missing_q_idx:
							q.insert(idx, None)

			answers.extend(questions)

		# Debug Display routine
		# Color boxes that are in same question similar
		if self.show_priority_threshold < 2:
			img = self.image.copy()
			for idx, answer in enumerate(answers):
				hue = 25 * idx % 180
				for idx2, box in enumerate(a for a in answer if a is not None):
					val = abs(255 - idx2 * 50) % 256
					[[color]] = cv2.cvtColor(numpy.uint8([[[hue, 255, val]]]), cv2.COLOR_HSV2BGR)
					color: numpy.ndarray
					cv2.rectangle(img, box.top_left, box.bottom_right, color=color.tolist(), thickness=2)
					cv2.putText(img, f'{box.value / box.area():.02f}', (box.x, box.y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
			
			self.show_image("Grouped Answers", img)

		# III. Evaluate checkboxes

		student = Student(0) # Id needs to be set by caller

		for answer in answers:
			options = ""
			for box in answer:
				if box is None:
					options += '#'
				else:
					ratio = box.value / box.area()
					for low, high, val in self.RATIOS:
						if low <= ratio < high:
							options += val
							break
					
			student.answers.append(Answer(options=options))
		
		return student
				
	@classmethod
	def canParse(cls, args: list[Any]) -> bool:
		return len(args) > 0 and Path(args[0]).suffix.lower() in ('.png',)

AnswerParser.register(PngParser)

from pathlib import Path

def test():
	pic = r'./pic/test_normal--000.png'
	
	parser = PngParser([pic])
	student = parser.extractAnswers()

	print(student)


if __name__ == "__main__":
	test()
