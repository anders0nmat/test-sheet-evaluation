# Documentation

This document gives a rough outline of the inner workings and structure of the program as well as a detailed introduction to extending on the programs functionality.

## Internal Operations

The program has the following inputs:
- `INPUT_FILE`
- `SOLUTION_FILE` (Optional)
- `SQL_LOCATION` (Default: `./`)
- `OUTPUT_FILE`

High-level order of operatios:

1. Find the corresponding parser for `INPUT_FILE` by calling `AnswerParser.getParser()`
	- This calls the `canParse()` class-method of registered parsers and returns the first parser that returns `True`
2. Parse `INPUT_FILE` through `parser.extractAnswers()`
	- This yields a `list[Student]`
3. Do step 1. and 2. for `SOLUTION_FILE` if present
	- Assert that at most one Student comes out of the solution file
	- Assign id as given by `-sid` CLI argument (Default: `0`)
	- Append result to list of Students
4. Call the `SqlAnalyzer`. Pass colleted list of Students and `SQL_LOCATION`
	- This yields a `StatisticsBook`, a simplified equivalent to an excel workbook
5. Find the correct printer for `OUTPUT_FILE` by calling `FilePrinter.getPrinter()`
	- This calls the `canPrint()` class-method of registered printers and returns the first printer that returns `True`
6. Print the StatisticsBook with the received Printer

## Data structures

Data structures are used as an abstracted way to exchange data between the different stages of the program. They are intentionally very simplified to ensure maximum compatibility with as many possible extensions as possible.

### Student

The `Student` structure holds all data related to one test sheet, commonly associated with one student. As such, it contains an identifier and a list of answers to test questions.

```python
class Student:
	id: int
	answers: list[Answer]
```

### Answer

The `Answer` structure contains all data for a particular question and student. This currently includes only a list of checkbox states represented as a string but might contain more data in the future.

```python
class Answer:
	options: str
```

### StatisticsBook

A `StatisticsBook` is an abstracted version of an excel workbook. It consists of a list of sheets.

```python
class StatisticsBook:
	sheets: list[StatisticsSheet]
```

### StatisticsSheet

A `StatisticsSheet` is the analog version of an excel sheet, containing a sheet name and a list of rows.

```python
class StatisticsSheet:
	name: str
	rows: list[StatisticsRow]
```

### StatisticsRow

A `StatisticsRow` contains values of a single row of a spreadsheet. Each value is represented as a string.

```python
class StatisticsRow:
	values: list[str]
```

## Extend TestAssist

There are three point of interest for extending TestAssist:

1. Input file formats
2. Analysis
3. Output (file) formats

### 1. Input file formats

To allow for new input file formats, create a class inheriting from `AnswerParser`.

You are required to implement the following functions:
- `extractAnswers(self) -> list[Student]`

Additionally, AnswerParser implements a factory-like pattern. You have to provide a `canPrint(cls, args: list[Any]) -> bool` class-method that indicates whether the parser is able to parse the desired file. `AnswerParser` provides a default convenience implementation that returns `True` if the file extension is in a class-wide set of extensions called `EXTENSIONS`.

The initializer will receive a single argument: `args: list[Any]` where the first entry is the `INPUT_FILE` as provided by the CLI. Other arguments may follow.

To make the parser available to the toolchain register it with `AnswerParser.register()`

Example for a new parser that receives a textfile with just a stream of answers, e.g. "ABBDACABDD":
```python
class TextParser(AnswerParser):
	# Used by the default implementation of canParse()
	EXTENSIONS = {'.txt', '.answers'}

	def __init__(self, args: list[Any]):
		file = args[0]
		self.content = file.read_text()

	def extractAnswers(self) -> list[Student]:
		result = []
		...
		return result

# Register for use in program
AnswerParser.register(TextParser)
```

### 2. Analysis

For more sophisticated analysis, you can inherit from the `AnswerStatistics` class, which requires you to implement a `analyze(self) -> StatisticsBook` function.

`self` already contains some convenience fields:
- `self.students` of type `list[Student]` contains all students
- `self.nerd` of type `Optional[Student]` contains `None` or one Student that is concidered to have all questions answered correctly (as provided by `-s` CLI argument)

Please be careful if you implement a custom `__init__` to call the parent initializer that populates the `.students` and `.nerd` fields.

To use your custom analyzer class, adjust the analyzer call in `__main__.py` in `STEP 3`.

Example with a new analysis step:
```python
class AverageStatistics(AnswerStatistics):
	def analyze(self) -> StatisticsBook:
		avg_sheet = StatisticsSheet(name="Averages")
		...
		return StatisticsBook(sheets=[avg_sheet])

# File __main__.py
[...]
	# STEP 3 : Analyze...

	statistics = SqlAnalyzer(students, nerd=nerd, sql_path=args.sql)
	avg_statistics = AverageStatistics(students, nerd=nerd)

	# Append sheets to existing Book
	statistics.sheets.extend(avg_statistics.sheets)
	book = statistics.analyze()

[...]
```

### 3. Output (file) formats

To customize output, you can inherit from the `StatisticsPrinter` class. This is a general abstraction with no assumptions about the type of output. If you plan to output a file, inherit from `FilePrinter` instead.

#### 3.1 StatisticsPrinter

The StatisticsPrinter is intended if you want to output the results in other means such as a web server, direct console printing or image display through matplotlib.

You are expected to provide a `printStatistics(self)` method that utilizes the `self.statBook` of type `StatisticsBook` to output to your desired format/medium.

Please be careful if you implement a custom `__init__` to call the parent initializer that populates the `.statBook` field.

To use your custom printer, please modify the section `STEP 4` in `__main__.py`.

Example of a simple console printer:
```python
class ConsolePrinter(StatisticsPrinter):
	def printStatistics(self):
		for sheet in self.statBook.sheets:
			print(f"Sheet '{sheet.name}'")
			for row in sheet.rows:
				print("\t" + ' ; '.join(row))

# File __main__.py
[...]
	# STEP 4 : Print results

	printer = ConsolePrinter(book)
	printer.printStatistics()

[...]
```

#### 3.2 FilePrinter

The FilePrinter is intended if you want to output the results as a file. It provides convenience functionality that you will likely need if you work wih files.

You are expected to provide a `printStatistics(self)` method that utilizes the `self.statBook` of type `StatisticsBook` to output to your desired file format.

`self` provides the following fields by default:
- `self.statBook` of type `StatisticsBook` contains the data to be outputted to a file
- `self.filePath` if type `pathlib.Path` contains the output path as provided by the `-o` CLI argument

Additionally, FilePrinter implements a factory-like pattern. You have to provide a `canPrint(cls, path: Path, book: StatisticsBook) -> bool` class-method that indicates whether the printer is able to output the desired file. `FilePrinter` provides a default convenience implementation that returns `True` if the file extension is in a class-wide set of extensions called `EXTENSIONS`.

Please be careful if you implement a custom `__init__` to call the parent initializer that populates the `.statBook` and `.filePath` fields.

To use your custom printer, please modify the section `STEP 4` in `__main__.py`.

Example of a text output printer:
```python
class TextPrinter(FilePrinter):
	# used by default implementation of canPrint()
	EXTENSIONS = {'.txt', '.analysis'}

	def printStatistics(self):
		out_lines = []
		for sheet in self.statBook.sheets:
			out_lines.append(f"Sheet '{sheet.name}'")
			for row in sheet.rows:
				out_lines.append("\t" + ' ; '.join(row))
		self.filePath.write_text("\n".join(out_lines))

# Register for use in program
FilePrinter.register(TextPrinter)
```


