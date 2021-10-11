"""
Date: 01/10/2021
Author: Matteo Nunziante
First version of a sudoku solver
"""

from enum import Enum
SIZE = 9


class State(Enum):
    """
    Create an enumerate list for the possible situation in a cell of the sudoku
        VALID   -> the number can be inserted
        INVALID -> the number cannot be inserted
        UNKNOWN -> it's not known if the number can or cannot be put in the cell
        SET     -> the number is been inserted
        OCCUPIED-> to indicate in a cell there is an other number
        DEFAULT -> the number is pre-defined by the game (inserted byt the user) (for the moment it isn't used)
    """
    VALID = 0
    INVALID = 1
    UNKNOWN = 2
    SET = 3
    OCCUPIED = 4
    DEFAULT = 5


class SudokuHandler:
    def __init__(self):
        self.size = SIZE  # 9x9 sudoku
        self.matrix = []  # This matrix will contain the numbers
        self.grid = []    # This is a set of matrix (one for each number) of value in State
        # Initialize the grid of matrices (one for each number)
        for _ in range(0 , self.size):
            self.grid.append(self.initMask())

    def initMask(self):
        """
        Method that initialize the generic matrix board to all UNKNOWN values
        :return: the new matrix initialized
        """
        # Initialize the matrix
        matrix = []
        for i in range(0 , self.size):
            row = []
            for j in range(0 , self.size):
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
            self.matrix.append(row)
            for j in range(0 , self.size):
                # self.matrix[i][j] = row[j]

                # If the user inserted a value
                if self.matrix[i][j] != "_":
                    # Save the integer
                    numberInserted = int(self.matrix[i][j])

                    k = 0
                    """
                    For every mask in self.grid, in the mask corresponding the number inserted put DEFAULT,
                        else OCCUPIED
                    """
                    for mask in self.grid:
                        if k == numberInserted:
                            # mask[i][j] = State.DEFAULT
                            mask[i][j] = State.SET
                        else:
                            mask[i][j] = State.OCCUPIED
                        k += 1

    def isPresentInArray(self , numberToFind , index , row = True):
        """
        Method used to search if a number is present in an array
        :param row: indicates if the index is referring to a row or to a column
        :param index: is the index of the row/column
        :param numberToFind: is the number to find
        :return: True if the number is present, False otherwise
        """
        for i in range(0 , self.size):
            if row:
                if self.matrix[index][i] == str(numberToFind):
                    return True
            else:
                if self.matrix[i][index] == str(numberToFind):
                    return True
        return False

    def isPresentInSquare(self , numberToFind , x , y):
        """
        Method used to search if a number is present in a sub-matrix (3x3)
        :param numberToFind: is the number to find
        :param x: is the coordinate x of the first cell in the sub-matrix
        :param y: is the coordinate y of the first cell in the sub-matrix
        :return: True if the number is present, False otherwise
        """
        for i in range(x , x + 3):
            for j in range(y , y + 3):
                if self.matrix[i][j] == str(numberToFind):
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

    def printGrid(self):
        """
        Method that print the mask matrices
        """
        number = 1
        for mask in self.grid:
            print("Mask of number " + str(number))
            for i in range(0 , self.size):
                for j in range(0 , self.size):
                    print(mask[i][j] , end = " ")
                print("")
            number += 1

    def isCompleted(self):
        """
        Method that checks if the matrix is full and completely
        :return: True if the matrix if full, False otherwise
        """

        # Verify if in every row/column is present every number between 0 and self.size
        for i in range(0 , self.size):
            for number in range(1 , self.size + 1):
                if not self.isPresentInArray(number , i):
                    return False
                if not self.isPresentInArray(number , i , False):
                    return False

        # Verify if in every sub-matrix is present every number between 0 and self.size
        subSpaces = [0 , 3 , 6]  # Starting indexes of the sub-matrix

        # For every number number, check in every sub-matrix
        for number in range(1 , self.size + 1):
            for row in subSpaces:
                for column in subSpaces:
                    if not self.isPresentInSquare(number , row , column):
                        return False

        return True

    def updateGrid(self , x = None , y = None):
        """
        Method that updates the grid after a number is been inserted
            (or as init of the grid during the first phase -> x , y not specified)
        :param x: is the coordinate x of the new number
        :param y: is the coordinate y of the new number
        """

        # If it's the first call
        if x is None and y is None:
            # Need to update the grid of every mask looking for every default number
            for i in range(0 , self.size):
                for j in range(0 , self.size):
                    if self.matrix[i][j] != "_":
                        # Call this function for the specific cell
                        self.updateGrid(i , j)

        # If a number is been inserted
        if x is not None and y is not None:
            numberInserted = int(self.matrix[x][y]) - 1  # The index for the grid

            k = 0
            # Notify every mask about the new number
            for mask in self.grid:
                if k != numberInserted:
                    mask[x][y] = State.OCCUPIED
                else:
                    mask[x][y] = State.SET
                k += 1

            # print("x is:" + str(x))
            # print("y is:" + str(y))
            # Notify the row/column that they are invalid in the mask corresponding the number inserted
            for i in range(0 , self.size):
                # if i != numberInserted:
                if (self.grid[numberInserted])[x][i] != State.OCCUPIED and \
                        (self.grid[numberInserted])[x][i] != State.SET:
                    (self.grid[numberInserted])[x][i] = State.INVALID
                if (self.grid[numberInserted])[i][y] != State.OCCUPIED and \
                        (self.grid[numberInserted])[i][y] != State.SET:
                    (self.grid[numberInserted])[i][y] = State.INVALID

            # Notify the whole sub-square that it is invalid in the mask corresponding the number inserted
            # Take the coordinate of the first cell in high-left of the sub-matrix
            x2 , y2 = self.takeSquare(x , y)

            for iRow in range(x2 , x2 + 3): # from x2 to x2 + 2 (x2 + 3 is excluded)
                for iCol in range(y2 , y2 + 3):
                    if (self.grid[numberInserted])[iRow][iCol] != State.OCCUPIED and \
                            (self.grid[numberInserted])[iRow][iCol] != State.SET:
                        (self.grid[numberInserted])[iRow][iCol] = State.INVALID

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
            y2 = 6

        return x2 , y2

    def insertANumber(self):
        """
        This method will perform the insertion of a new number
            It will search for the right place where put the number
        :return: True if the algorithm inserted a number, False if it couldn't
        """

        # Check all the masks in self.grid
        for m in range(1 , self.size + 1):
            # Check the row
            for i in range(0 , self.size):
                validPosition = 0
                for j in range(0 , self.size):
                    if ((self.grid[m - 1])[i][j] == State.VALID or (self.grid[m - 1])[i][j] == State.UNKNOWN)\
                            and not self.isPresentInArray(m , i):
                        validPosition += 1
                # If there is just one position valid/unknown -> insert the m number in that position
                if validPosition == 1:
                    for j in range(0, self.size):
                        if (self.grid[m - 1])[i][j] == State.VALID or (self.grid[m - 1])[i][j] == State.UNKNOWN:
                            y = j
                    # Add the number in the main matrix
                    print("R: inserted " + str(m) + " in position " + str(i) + "," + str(y))
                    self.matrix[i][y] = str(m)
                    # Update the grid
                    self.updateGrid(i , y)
                    return True

            # Check the column
            for i in range(0 , self.size):
                validPosition = 0
                for j in range(0 , self.size):
                    if ((self.grid[m - 1])[j][i] == State.VALID or (self.grid[m - 1])[j][i] == State.UNKNOWN) \
                            and not self.isPresentInArray(m , i , False):
                        validPosition += 1
                # If there is just one position valid/unknown -> insert the m number in that position
                if validPosition == 1:
                    for j in range(0, self.size):
                        if (self.grid[m - 1])[j][i] == State.VALID or (self.grid[m - 1])[j][i] == State.UNKNOWN:
                            x = j
                    # Add the number in the main matrix
                    print("C: inserted " + str(m) + " in position " + str(x) + "," + str(i))
                    self.matrix[x][i] = str(m)
                    # Update the grid
                    self.updateGrid(x , i)
                    return True

            # Check the sub-matrices -> (i , j) is the first cell of the current sub-matrix
            for i in range(0 , self.size , 3):
                for j in range(0, self.size, 3):
                    validPosition = 0
                    for i2 in range(0 , 3):
                        for j2 in range(0 , 3):
                            if ((self.grid[m - 1])[i + i2][j + j2] == State.VALID or \
                                    (self.grid[m - 1])[i + i2][j + j2] == State.UNKNOWN)\
                                    and not self.isPresentInSquare(m , i , j):
                                validPosition += 1
                    # If there is just one position valid/unknown -> insert the m number in that position
                    if validPosition == 1:
                        for i2 in range(0, 3):
                            for j2 in range(0, 3):
                                if (self.grid[m - 1])[i + i2][j + j2] == State.VALID or \
                                        (self.grid[m - 1])[i + i2][j + j2] == State.UNKNOWN:
                                    x = i + i2
                                    y = j + j2
                        print("S: inserted " + str(m) + " in position " + str(x) + "," + str(y))
                        self.matrix[x][y] = str(m)
                        # Update the grid
                        self.updateGrid(x , y)
                        return True

        # If nothing has been added
        return False

    def process(self):
        """
        This is the main function that handler the algorithm
        """
        # Read the game
        self.readMatrix()
        # Update the masks
        # print("Length of the grid is: " + str(len(self.grid)))
        # print("Length of a mask is: " + str(len(self.grid[0])))
        # print("Depth of a mask is: " + str(len(self.grid[0][0])))
        self.updateGrid()
        self.printMatrix()
        # self.printGrid()

        while not self.isCompleted():
            # Insert a number
            result = self.insertANumber()
            if not result:
                print("It's not possible to find a solution")
                # print(self.printGrid())
                return
            # Show the new matrices
            self.printMatrix()
            # self.printGrid()
        print("The computation ended correctly")


if __name__ == "__main__":
    sudokuHandler = SudokuHandler()
    sudokuHandler.process()



