# coding: utf8
"""
Description:
    Contains the Area class
Classes:
    Area: Represents a zone of a Sudoku. Contains 9 cells, each with a different data/number.
"""


# --------------------------------------------------------------------------------
# > Imports
# --------------------------------------------------------------------------------
# Built-in

# Third-party

# Local
from classes.cell import Cell


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class Area:
    """
    Description:
        Represents a zone of a Sudoku. Contains 9 cells, each with a different data/number.
        Two Cells of an Area cannot contain the same number (between 1 and 9)
        A Sudoku instance will have 27 Area instances : 9 rows, 9 columns, 9 squares

    Constants:
        SHAPES (set): Sets of string, representing the type of Area

    Magic Methods:
        __init__: Initializes the Area instance
        __iter__: Iterates over the list of cells (self.cells)
        __len__: Returns the quantity of cell with valid data
        __repr__: Returns a string representation of our Area instance, without its cells

    Attributes:
        cells (list): List of Cell instances in the Area
        shape (string): String that indicates the type of Area. Is a value of self.SHAPES.
        num (int): The index of the Area within the Sudoku, within the list of same shapes

    Properties:
        available_numbers (set): Dynamically lists the numbers not yet written in its cells
        taken_numbers (set): Dynamically finds all the numbers already written its cells
    """

    ###############
    #  Constants  #
    ###############
    SHAPES = {"row", "column", "square"}

    ###################
    #  Magic Methods  #
    ###################
    def __init__(self, cell_list, shape, num):
        """
        Description:
            Initializes the Area instance
            Using "shape" and "num", we can easily guess which part of the Sudoku the Area instance represents
        Args:
            cell_list (list): List of Cell instances stored in the area
            shape (str): Either "row", "column", or "square"
            num (int): Index or position of the area
        Raises:
            KeyError: "shape" must be either "row", "column", or "square". See "self.SHAPES"
        """
        if shape not in self.SHAPES:
            raise KeyError(
                "'{}' is not a valid shape for an Area instance".format(shape)
            )
        self.cells = cell_list
        self.shape = shape
        self.num = num

    def __iter__(self):
        """Iterates over the instance's cells"""
        return iter(self.cells)

    def __len__(self):
        """Returns the quantity of cell with valid data"""
        return len(self.taken_numbers)

    def __repr__(self):
        """Returns a string representation of our Area instance, without its cells"""
        return "Area(shape='{}', num={})".format(self.shape, self.num)

    ################
    #  Properties  #
    ################
    @property
    def available_numbers(self):
        """Property that returns a set of the numbers that can be written in the Area"""
        return Cell.NUMBERS - self.taken_numbers

    @property
    def taken_numbers(self):
        """Property that returns a set of all the numbers already written in the Area"""
        numbers = set()
        for cell in self:
            if cell.data is not None:
                numbers.add(cell.data)
        return numbers
