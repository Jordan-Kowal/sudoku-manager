# coding: utf8
"""
Description:
    Contains the Cell class
Classes:
    Cell: Cell of a Sudoku instance that contains a number between 1 and 9
"""


# --------------------------------------------------------------------------------
# > Imports
# --------------------------------------------------------------------------------
# Built-in

# Third-party

# Local


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class Cell:
    """
    Description:
        Cell of a Sudoku instance that contains a number between 1 and 9
        A Sudoku instance should be made of 81 Cell instances

    Constants:
        NUMBERS (set): Set of valid data for a Cell (numbers from 1 to 9)
        NUMBERS_NONE (set): Same as NUMBERS, but inclues "None" in the dataset

    Magic Methods:
        __init__: Initiliazes a Cell instance and stores its coordinates
        __repr__: Returns a string representation of our Cell instance

    Attributes:
        areas (list): List of the 3 Area instances our cell is in
        column (int): Index of the sudoku column where our cell is
        data (int): Value contained in the cell. Either "None" or a number between 1 and 9
        row (int): Index of the sudoku row where our cell is
        square (int): Index of the sudoku square/box where our cell is
    """

    ###############
    #  Constants  #
    ###############
    NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    NUMBERS_NONE = {1, 2, 3, 4, 5, 6, 7, 8, 9, None}

    ###################
    #  Magic Methods  #
    ###################
    def __init__(self, row, column, square, data=None):
        """
        Description:
            Initializes our Cell instance
            If "data" is not a number between 1 and 9, it will be changed to None
        Args:
            areas (list): List of 3 Area instances the cell is part of
            row (int): Index of the sudoku row where our cell is
            column (int): Index of the sudoku column where our cell is
            square (int): Index of the sudoku square/box where our cell is
            data (int, optional): Number contained in the cell. Defaults to None.
        """
        try:
            data = int(data)
        except (ValueError, TypeError):
            pass
        if data not in self.NUMBERS:
            data = None
        self.data = data
        self.areas = []
        self.row = row
        self.column = column
        self.square = square

    def __repr__(self):
        """Returns a string representation of our Cell instance"""
        return "Cell(data={data}, row={row}, column={column}, square={square})".format(
            **vars(self)
        )

    # ! Adds data integrity but slows down the solving process for the Sudoku instance
    # def __setattr__(self, name, value):
    #     """Overrides the "setattr" function to check if data gets a valid input"""
    #     if name == "data":
    #         if value not in self.NUMBERS_NONE:
    #             raise ValueError("'data' property value must be a number between 1 and 9")
    #     super().__setattr__(name, value)
