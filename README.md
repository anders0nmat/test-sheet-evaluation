# TestAssist

## Overview

TestAssist is a Python-based utility designed for processing multiple-choice test sheets. It automates the following key tasks:

1. Conversion of PDF pages to PNG images.
2. Image analysis using OpenCV to extract marked answer boxes.
3. Convert extracted data to in-memory SQL database.
4. Execution of user-provided queries for data analysis.
5. Export of query results to various formats.

This tool is easily extensible, allowing users to define new input formats, output formats, or analysis stages by inheriting from the provided abstract classes. See more in the [Extend TestAssist](DOCS.md#extend-testassist) section.

## Installation

To install and run TestAssist, you need the following libraries:

- [Python](https://www.python.org/downloads/) (3.10 or newer) including pip
- Poppler (See [Install Poppler](#install-poppler) for instructions)

Steps to install/run:

1. [Download](/releases/latest) the latest release `.zip`.
2. Unpack.
3. Install required python packages with
	```shell
	pip install -r requirements.txt 
	```
	(Note: Make sure you are running this in the unzipped folder)

To run the program, see [Usage](#usage).

### Install Poppler

For Windows: 
- Go to [poppler-windows on GitHub](https://github.com/oschwartz10612/poppler-windows) and download the latest release `.zip`
- Unpack at a location of your choice
- Add the `/Library/bin/` path of the unpacked zip folder to your windows PATH environment variable.

For Linux:
- Poppler is probably preinstalled on your distribution. To check, open a terminal and execute `pdfinfo`. You should see a description of how to use the command. If not, proceed with the steps
- Install the `poppler-utils` package from your distributions' package manager
  
For Mac:
- [Install brew](https://brew.sh/)
- Execute
	```shell
	brew install poppler
	```

## Prerequisites

Possible formats:
- Input: `.csv`, `.png`, `.pdf`
- Analysis: `.sql`
- Output: `.csv`, `.xlsx`

This list is [extensible](DOCS.md#extend-testassist).

## Usage

To run TestAssist, open a terminal in the unpacked folder and run:

```shell
python src SHEETS -o OUTPUT -s SOLUTION -sid INTEGER -q SQL -c COUNT
```

Argument | Required | Description
-- | -- | --
`SHEETS` | Yes | Path to a single sheet file
`-o OUTPUT` or `--output OUTPUT` | Yes | Name of the output file. The file extension determines the output format
`-s SOLUTION` or `--solution SOLUTION` | No | Path to a solution file. Treated as a normal test sheet with id of `0` (Changable)
`-sid INTEGER` or `--solution-id INTEGER` | No | Sets the id of solution sheet student to `INTEGER`. Defaults to `0`
`-q SQL` or `--sql` | No | Directory where `*.sql` queries are located or file containing query. Defaults to current working directory
`-c COUNT` or `--count COUNT` | No | Specifies how many answer options are available. Default: `4`


Example commands:
```shell
python src ./sheets/all_tests.pdf -o results.xlsx -q ./queries -s ./sheets/solution.csv
```

```shell
python src ./sheets/all_tests.pdf -o analysis.csv
```

## Documentation

For detailed order of operations and extensibility notes, see [Documentation](DOCS.md)

