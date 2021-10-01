"""
Date: 01/10/2021
Author: Matteo Nunziante
First version of a sudoku solver
"""

import enum

SIZE = 9


class State(enum):
    """
    Create an enumerate list for the possible situation in a cell of the sudoku
        VALID   -> the number can be inserted
        INVALID -> the number cannot be inserted
        UNKNOWN -> it's not known if the number can or cannot be put in the cell
        SET     -> the number is been inserted
        OCCUPIED-> to indicate in a cell there is an other number
        DEFAULT -> the number is pre-defined by the game (inserted byt the user)
    """
    VALID = 0
    INVALID = 1
    UNKNOWN = 2
    SET = 4
    OCCUPIED = 5
    DEFAULT = 6


class SudokuHandler:
    def __init__(self):
        self.size = SIZE  # 9x9 sudoku
        self.matrix = []  # This matrix will contain the numbers
        # Initialize the matrix
        self.matrix = self.initMask()
        self.grid = []    # This is a set of matrix (one for each number) of value in State
        # Initialize the grid of matrices (one for each number)
        for _ in self.size:
            self.grid.append(self.initMatrix())

    def initMatrix(self):
        """
        Method that initialize the generic matrix board to all UNKNOWN values
        :return: the new matrix initialized
        """
        # Initialize the matrix
        matrix = []
        for i in range(0 , self.size - 1):
            row = []
            for j in range(0 , self.size - 1):
                # Set the unknown state in every cell
                row.append(State.UNKNOWN)
            matrix.append(row)
        return matrix

    def readMatrix(self):
        """
        Method used to read from the command line the matrix to initialize self.matrix and ,as consequence, self.grid
        """
        print("Insert the sudoku board: insert 1 line per time")

        # Read from the input
        for i in range(0 , self.size):
            row = input().split(" ")
            for j in range(0 , self.size):
                self.matrix[i][j] = row[j]

                # If the user inserted a value
                if self.matrix[i][j] != " ":
                    # Save the integer
                    numberInserted = int(self.matrix[i][j])

                    k = 0
                    """
                    For every mask in self.grid, in the mask corresponding the number inserted put DEFAULT,
                        else OCCUPIED
                    """
                    for mask in self.grid:
                        if k == numberInserted:
                            mask[i][j] = State.DEFAULT
                        else:
                            mask[i][j] = State.OCCUPIED
                        k += 1

    def isPresentInArray(self , numberToFind , array):
        """
        Method used to search if a number is present in an array
        :param numberToFind: is the number to find
        :param array: is the row/column of the matrix according to the situation
        :return: True if the number is present, False otherwise
        """
        for elem in array:
            if numberToFind == elem:
                return True
        return False

    def isPresentInSquare(self , numberToFind , mtr):
        """
        Method used to search if a number is present in a sub-matrix (3x3)
        :param numberToFind: is the number to find
        :param mtr: is the sub-matrix
        :return: True if the number is present, False otherwise
        """
        for row in mtr:
            for i in range(0 , len(mtr)):
                if row[i] == numberToFind:
                    return True
        return False

    def printMatrix(self):
        """
        Print the matrix self.matrix
        """
        for row in self.matrix:
            for cell in row:
                print(cell , end = " ")
            print("")

    def isCompleted(self):
        """
        Method that checks if the matrix is full and completely
        :return: True if the matrix if full, False otherwise
        """

        # Verify if in every row/column is present every number between 0 and self.size
        for i in range(0 , self.size):
            for number in range(0 , self.size):
                if not self.isPresentInArray(number , self.matrix[i]):
                    return False
                if not self.isPresentInArray(number , self.matrix[:][i]):
                    return False

        # Verify if in every sub-matrix is present every number between 0 and self.size
        subSpaces = [0 , 3 , 6]  # Starting indexes of the sub-matrix

        # For every number number, check in every sub-matrix
        for number in range(0 , self.size):
            for row in subSpaces:
                for column in subSpaces:
                    if not self.isPresentInSquare(number , self.matrix[row , row + 2][column , column + 2]):
                        return False

        return True

    def updateGrid(self , x = None , y = None):
        """
        Method that updates the grid after a number is been inserted
            (or as init of the grid during the first phase -> x , y not specified)
        :param x: is the coordinate x of the new number
        :param y: is the coordinate y of the new number
        """

        # If a number is been inserted
        if x is not None and y is not None:
            numberInserted = int(self.matrix[x][y])  # The index for the grid

            k = 0
            # Notify every mask about the new number
            for mask in self.grid:
                if k != numberInserted:
                    mask[x][y] = State.OCCUPIED
                k += 1

            # Notify the row/column that they are invalid in the mask corresponding the number inserted
            for i in range(0 , self.size):
                if i != numberInserted:
                    self.grid[numberInserted][x][i] = State.INVALID
                    self.grid[numberInserted][i][y] = State.INVALID
                else:
                    self.grid[numberInserted][x][i] = State.SET

            # Notify the whole sub-square that it is invalid in the mask corresponding the number inserted
            # Take the coordinate of the first cell in high-left of the sub-matrix
            x2 , y2 = self.takeSquare(x , y)

            for iRow in range(x2 , x2 + 2):     #  self.grid[numberInserted][x2 : x2 + 2][y2 : y2 + 2]:
                for iCol in range(y2 , y2 + 2):
                    if self.grid[numberInserted][iRow][iCol] != State.OCCUPIED:
                        self.grid[numberInserted][iRow][iCol] = State.INVALID

    def takeSquare(self , x , y):
        """
        Given the coordinate x,y return the first index of the sub-matrix
        :param x: is the x coordinate
        :param y: is the y coordinate
        :return: a tuple of coordinates
        """
        x2 , y2 = 0 , 0

        if x < 3:
            x2 = 0
        elif x < 6:
            x2 = 3
        else:
            x2 = 6

        if y < 3:
            y2 = 0
        elif y < 6:
            y2 = 3
        else:
            y = 6

        return x2 , y2

    def process(self):
        """
        This is the main function that handler the algorithm
        """
        # Read the game
        self.readMatrix()

        while not self.isCompleted():
            self.printMatrix()


if __name__ == "__main__":
    sudokuHandler = SudokuHandler()
    sudokuHandler.process()



