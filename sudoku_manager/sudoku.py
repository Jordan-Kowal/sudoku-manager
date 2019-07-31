# coding: utf8
"""
Description:
    Contains the Sudoku class
Classes:
    Sudoku: Sudoku generator and solver
"""


# --------------------------------------------------------------------------------
# > Imports
# --------------------------------------------------------------------------------
# Built-in
import json
import os
from random import choice, seed
from time import perf_counter

# Third-party

# Local
from classes.area import Area
from classes.cell import Cell


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class Sudoku:
    """
    Description:
        Sudoku generator and solver
        Sudoku grids can be generated from scratch or given as input
        The class can be used to generate and/or solve sudokus
        The instance stores metrics regarding the solving process
        The Sudoku instance is made of 27 Area instances and 81 Cell instances where
        - Areas are rows, columns, and squares
        - Cells are individuall cells/inputs

    Constants:
        ACTIONS (list): List of actions names that we will use in "history" and "complete_history"
        COL_SEP (str): Column separator used when printing the sudoku grid
        DIFFICULTIES (dict): Dict of difficulties, each containing a dict with: name, min_time, max_time, empty_cells
        ROW_SEP (str): Row separator used when printing the sudoku grid

    Magic Methods:
        __init__: Checks if "grid" has a valid shape and initializes our Sudoku instance
        __iter__: Iterates over the cells of the Sudoku instance
        __repr__: Returns a string representation of the Sudoku instance

    Public Methods:
        display: Returns a string shaped like our Sudoku
        display_row: Returns a string shaped like a Sudoku row for said row
        generate_areas: Creates the 27 Area instances (9 rows, 9 columns, 9 squares)
        generate_cells: Generates and stores the 81 Cell instances based on the initial grid
        get_available_cell_values: Gets the values that can be written in the cell, based on the sudoku rules
        shape_is_valid: Checks if the initial grid is a list of 9-element lists
        solve: Starts a timer and tries to solve the sudoku
        undo: Takes care of the backtracking by undoing previous actions
        write_and_log: Writes down a number in a Cell, and log the action in the history logs

    Attributes:
        areas (list): List containing the 27 Area instances, in order
        cells (list): List containing the 81 Cell instances, in order
        columns (list): List containing the 9 Area instances representing the columns, in order
        complete_history (list): Complete history of every action made during the solving process
        empty_cells (list): List of empty cells in the Sudoku. Updated at every move
        grid (list): The initial 9x9 list that created the instance
        history (list): Same as "complete_history", but "undo" is not logged and removes the last entry
        moves (int): The number of moves made (but "undo" removes a move)
        required_moves: The number of empty cells in the initial grid. Used for "self.solved"
        rows (list): List containing the 9 Area instances representing the rows, in order
        solved_grid (list): The solved Sudoku in a 9x9 format
        squares (list): List containing the 9 Area instances representing the squares, in order
        status (str): Information regarding the state of the solving process
        total_moves (int): Total number of moves made (move = writing something in a cell)

    Properties:
        metrics (dict): Dict containing the following attributes: solved, status, time, required_moves, total_moves
        solved (bool): Property that indicates if the sudoku is solved

    Class Methods:
        create_from_81: Creates a Sudoku instance using a 81-element list instead of a 9x9 list
        create_from_json: Creates a Sudoku from a grid stored in a JSON file
        generate_grid: Loops until a valid sudoku is generated, based on the difficulty settings

    Static Methods:
        output_as_json: Jsonify the data and writes in the file at the given path
    """

    ###############
    #  Constants  #
    ###############
    ACTIONS = ["write", "undo"]
    DIFFICULTIES = {
        1: {"name": "easy", "min_time": 0.000, "max_time": 0.005, "empty_cells": 45},
        2: {"name": "medium", "min_time": 0.005, "max_time": 0.010, "empty_cells": 52},
        3: {"name": "hard", "min_time": 0.010, "max_time": 0.020, "empty_cells": 59},
        4: {"name": "harder", "min_time": 0.020, "max_time": 0.040, "empty_cells": 66},
        5: {"name": "hardest", "min_time": 0.040, "max_time": 0.060, "empty_cells": 70},
    }
    COL_SEP = "|"
    ROW_SEP = "------|-------|------"

    ###################
    #  Magic Methods  #
    ###################
    def __init__(self, grid):
        """
        Description:
            Checks if "grid" has a valid shape and initializes our Sudoku instance
        Args:
            grid (list): List of lists, where each sublist has 9 elements. Basically a 9x9 grid
        Raises:
            IndexError: Returned if the "grid" arg is not a 9x9 list
        """
        # Checking "grid" shape
        self.grid = grid
        if not self.shape_is_valid():
            raise IndexError("The 'grid' argument must be a 9x9 list")
        # Generating Cell and Area instances
        self.generate_cells()
        self.generate_areas()
        # Creating the other attributes
        self.empty_cells = [cell for cell in self if cell.data is None]
        self.required_moves = len(self.empty_cells)
        self.moves = 0
        self.total_moves = 0
        self.history = []
        self.complete_history = []

    def __iter__(self):
        """Iterates over the cells of the Sudoku instance"""
        return iter(self.cells)

    def __repr__(self):
        """Returns a string representation of the Sudoku instance"""
        return "Sudoku()"

    ####################
    #  Public Methods  #
    ####################
    def display(self):
        """Returns a string shaped like our Sudoku"""
        sudoku_string = ""
        for i in range(9):
            # Every third row, we add a separator
            if i % 3 == 0 and i > 0:
                sudoku_string += self.ROW_SEP
                sudoku_string += "\n"
            sudoku_string += self.display_row(i)
            sudoku_string += "\n"
        return sudoku_string

    def display_row(self, row_index):
        """
        Description:
            Returns a string shaped like a Sudoku row for said row
        Args:
            row_index (int): Index of the row we want to visualize
        Returns:
            str: String representation of our row
        """
        row_string = ""
        for i, cell in enumerate(self.rows[row_index]):
            # Every third cell, we had a seperator
            if i % 3 == 0 and i > 0:
                row_string += self.COL_SEP
                row_string += " "
            # Empty cells are represented as "." on the grid
            if cell.data is None:
                row_string += "."
            else:
                row_string += str(cell.data)
            row_string += " "
        row_string.strip()
        return row_string

    def generate_areas(self):
        """
        Description:
            Creates the 27 Area instances (9 rows, 9 columns, 9 squares)
            Each Area will contain a total of 9 Cell instance
            Meaning each Cell instance will be in 3 Areas: 1 row, 1 column, 1 square
            All the areas are then stored as attributes
        """
        # Grouping the cells
        cells_by_rows = [[cell for cell in self if cell.row == i] for i in range(9)]
        cells_by_columns = [[cell for cell in self if cell.column == i] for i in range(9)]
        cells_by_squares = [[cell for cell in self if cell.square == i] for i in range(9)]
        # Creating the different areas and storing them
        self.rows = [Area(cell_list, "row", i) for i, cell_list in enumerate(cells_by_rows)]
        self.columns = [Area(cell_list, "column", i) for i, cell_list in enumerate(cells_by_columns)]
        self.squares = [Area(cell_list, "square", i) for i, cell_list in enumerate(cells_by_squares)]
        self.areas = self.rows + self.columns + self.squares
        # Linking the Cell instances to their 3 Area instances
        for cell in self:
            cell.areas = [
                self.rows[cell.row],
                self.columns[cell.column],
                self.squares[cell.square],
            ]

    def generate_cells(self):
        """Generates and stores the 81 Cell instances based on the initial grid"""
        self.cells = []
        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                area = (x // 3) * 3 + (y // 3)
                value = self.grid[x][y]
                cell = Cell(x, y, area, value)
                self.cells.append(cell)

    def get_available_cell_values(self, cell):
        """
        Description:
            Gets the values that can be written in the cell, based on the sudoku rules
            A value can be written only if it does not already exist in the cell's row, column, and square
            So for a given cell, we check the content of its 3 Area instances
        Args:
            cell (Cell): A Cell instance from the Sudoku
        Returns:
            set: Set of values that can be written in the Cell
        """
        available_values = Cell.NUMBERS.copy()
        for area in cell.areas:
            available_values -= area.taken_numbers
        return available_values

    def shape_is_valid(self):
        """Checks if the initial grid is a list of 9-element lists"""
        if len(self.grid) == 9:
            for row in self.grid:
                if len(row) != 9:
                    return False
        return True

    def solve(self, randomly=False, time_limit=None):
        """
        Description:
            Description:
            Starts a timer and tries to solve the sudoku.
            We go through empty cells and tries the available inputs.
            In case of failure, the backtrack to our previous action
            The logic is as follows:
            - Get the FIRST empty cell
            - Check what we can write in it
            - Write the first available value (or a random one if "randomly=True")
            - Log in the "history" the cell, the value, and the other possible values
            - Remove said cell from the empty list
            - Move on to the next cell
            - If a cell has no possible value, "undo" the previous action and try a different number
            The Sudoku is solved if there are no empty cell left
            The Sudoku is unsolvable if we try to "undo" when there is no move in the archive
            "randomly" often slows down the solving process, but is useful for generating new Sudokus
        Args:
            randomly (bool, optional): If True, randomly choses the value to input (instead of the first one). Defaults to False.
            time_limit (float, optional): Stops the solving process after N seconds. Defaults to None.
        """
        self.time = perf_counter()
        seed()
        while not self.solved:
            if time_limit and float(time_limit) <= (perf_counter() - self.time):
                self.status = "time_limit_exceeded"
                break
            # We arbitrarily get the first empty cell
            cell = self.empty_cells[0]
            values = self.get_available_cell_values(cell)
            # Having no values mean we are stuck and must backtrack
            if len(values) == 0:
                fail = self.undo()
                # If we can't backtrack anymore, it means we've tried every possible combinaion
                if fail:
                    self.status = "no_valid_solution"
                    break
            else:
                self.empty_cells.pop(0)  # Update the "empty_cells" list
                if randomly:
                    value = choice(list(values))
                    values.remove(value)
                else:
                    value = values.pop()  # Removes and returns one of the values
                self.write_and_log(cell, value, values)
        # We time the process regardless of the outcome
        self.time = round(perf_counter() - self.time, 4)
        self.status = "solved"
        self.solved_grid = [[cell.data for cell in self.cells[i:i+9]] for i in range(0, 81, 9)]

    def undo(self):
        """
        Description:
            Takes care of the backtracking by undoing previous actions
            Goes in the history log, finds the last moves, and undo it
            If other values for the cell were available, tries one of them
            Else, goes back once more (and so on)
        Returns:
            bool: Returns True if it cannot backtrack anymore, meaning it is unsolvable
        """
        self.moves -= 1
        # Get the last action from the history log
        try:
            _, cell, _, available_values = self.history.pop()
            action = self.ACTIONS[1]
            self.complete_history.append((action, cell, cell.data, available_values))
        # If no action available, it means we've tried everything
        except IndexError:
            return True
        # If we have no more values for the cell, we put it back to "None" and go back one move
        if len(available_values) == 0:
            cell.data = None
            self.empty_cells.insert(0, cell)  # Insert it back in the "empty_cells" list
            self.undo()
        # Else, we try one of the other values
        else:
            value = available_values.pop()
            self.write_and_log(cell, value, available_values)

    def write_and_log(self, cell, data, other_available_values):
        """
        Description:
            Writes down a number in a Cell, and log the action in the history logs
            Also increments the move counters
        Args:
            cell (Cell): The Cell instance we want to write in
            data (int): The number from 1 to 9 to put in the cell
            other_available_values (set): All the other possible/valid values for this cell
        """
        # Increments the moves
        self.moves += 1
        self.total_moves += 1
        # Changes the cell value
        cell.data = data
        # Logs the actions in both histories
        action = self.ACTIONS[0]
        self.history.append((action, cell, data, other_available_values))
        self.complete_history.append((action, cell, data, other_available_values))

    ################
    #  Properties  #
    ################
    @property
    def metrics(self):
        return {
            "solved": self.solved,
            "status": self.status,
            "time": self.time,
            "required_moves": self.required_moves,
            "total_moves": self.total_moves,
        }

    @property
    def solved(self):
        """Property that indicates if the sudoku is solved"""
        return self.moves == self.required_moves

    ###################
    #  Class Methods  #
    ###################
    @classmethod
    def create_from_81(cls, array):
        """
        Description:
            Creates a Sudoku instance using a 81-element list instead of a 9x9 list
            This method will reshape the array into a 9x9 grid and create the Sudoku instance
        Args:
            array (list): List containing 81 elements
        Raises:
            IndexError: Whenever the "array" does not contain exactly 81 elements
        Returns:
            Sudoku: The Sudoku instance created from the array
        """
        if len(array) != 81:
            raise IndexError("The list must contain 81 elements")
        grid = [array[i:i+9] for i in range(0, 81, 9)]
        return cls(grid)

    @classmethod
    def create_from_json(cls, filepath):
        """
        Description:
            Creates a Sudoku from a grid stored in a JSON file
            The JSON file must be formated like the ones in "self.generate_sudoku_as_json()"
        Args:
            filepath (str): Absolute or relative path to the JSON file
        Returns:
            Sudoku: The Sudoku instance created from the grid in the JSON file
        """
        if os.path.isfile(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                unsolved_grid = data["unsolved"]
        return cls(unsolved_grid)

    @classmethod
    def generate_grid(cls, level, path=None, to_json=False):
        """
        Description:
            Loops until a valid sudoku is generated, based on the difficulty settings
            The logic is as follows:
            - We randomly populate the 0th, 4th and 8th squares of the sudoku (as they are independant)
            - We then solve the sudoku using the Sudoku class
            - We get the updated/full grid and randomly remove N numbers (based on difficulty)
            - We try solving it again, and time the process
            - If the solving is either too short or too long, we start from the beginning
            Once the timing is OK, we will save the starting grid and output it as JSON
        Args:
            level (int): The difficulty of the sudoku
            path (str, optional): Output path for the JSON file. Only useful is to_json==True. Default to None.
            to_json (bool, optional): Indicates if the grid should be output in a JSON file instead of returned. Default to False.
        Raises:
            KeyError: 'level' argument must be in Sudoku.DIFFICULTIES.keys()
        """
        # Checking the "level" input
        if level not in {1, 2, 3, 4, 5}:
            raise KeyError("'level' argument must be in Sudoku.DIFFICULTIES.keys()")
        while True:
            # Generating numbers for the squares 1, 5 and 9
            seed()
            grid = [[0 for i in range(9)] for j in range(9)]
            for i in range(0, 9, 3):
                numbers = list(Cell.NUMBERS)
                for x in range(i, i + 3):
                    for y in range(i, i + 3):
                        number = choice(numbers)
                        numbers.remove(number)
                        grid[x][y] = number
            # Solving the grid in random order, to have a new
            sudoku = cls(grid)
            sudoku.solve(randomly=True)
            solved_grid = sudoku.solved_grid.copy()
            # Randomly removing numbers from the grid
            new_grid = solved_grid.copy()
            level_info = cls.DIFFICULTIES[level]
            coordinates = [(x, y) for x in range(9) for y in range(9)]
            for i in range(level_info["empty_cells"]):
                pos = choice(coordinates)
                coordinates.remove(pos)
                x, y = pos
                new_grid[x][y] = None
            # Trying to solve it again
            sudoku = Sudoku(new_grid)
            sudoku.solve(time_limit=level_info["max_time"])
            # If solved in time, then we output it as JSON, else we restart the process
            if sudoku.solved and sudoku.time >= level_info["min_time"]:
                if to_json:
                    data = {"unsolved": new_grid, "solved": sudoku.solved_grid.copy()}
                    cls.output_as_json(data, path)
                    return
                else:
                    return new_grid

    ####################
    #  Static Methods  #
    ####################
    @staticmethod
    def output_as_json(data, path):
        """Jsonify the data and writes in the file at the given path"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
