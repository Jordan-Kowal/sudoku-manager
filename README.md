# Sudoku Manager

## **Description**
This package is made for easy sudoku generation and solving. Using the main Sudoku class, you'll easily be able to generate random sudoku (with a difficulty setting), load existing sudokus from different formats, and solve those sudokus. The sudoku class has attributes dedicated to performance and traceback, allowing you to study its behavior.

## **What it contains**
The module contains 3 classes:
- Sudoku: this is the main class you'll be using. It represents a sudoku grid.
- Area: An area represents either a row, a column, or a square in a sudoku grid. It contains Cell instances, and is used to easily check "which values can be written"
- Cell: A single cell in a sudoku grid. There are 81 in a 9x9 sudoku, and each Cell is associated with 3 Area instances (1 row, 1 column, 1 square)

Note that :
- A Sudoku instance is made of 27 Area instances: 9 rows, 9 columns, and 9 squares
- A Sudoku instance is made of 81 Cell instances
- An Area instance is made of 9 Cell instances
- Each Cell instance is stored into 3 areas (1 row, 1 column, and 1 square)

## **How it works**
- **To generate a sudoku**: simply call the `Sudoku.generate_as_json()` method with the correct settings. You will then have a grid in a JSON format
- **To solve a sudoku**: create a Sudoku instance (either from the normal constructor or a classmethod) and use the `.solve()` method to solve it
