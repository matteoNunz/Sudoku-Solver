"""
Date: 14/10/2021
Author: Matteo Nunziante
Sudoku solver

Structure used:
- matrix: the configuration of the sudoku
- grid: a list of 9 matrices, one for each number, made by State element
        -> it says if a number can go in a position or not

If it's impossible to solve the puzzle with the known criteria, the algorithm will try to fill it
    randomly, inserting the number that:
        - have the most number of VALID positions (low level of efficiency)
        - have the most number of element inserted (high level of efficiency)
    Furthermore in that case other two structures are used:
        - openList: to keep the configuration to be expanded (expanding = add a random number where it's possible)
        - closedList: to keep trace of all the numbers already expanded (to avoid repetition/cycle)

To run the algorithm insert the sudoku in a text file (for example in the directory "Sudoku-Example") and modify
    the method readMatrix with the right path

In the directory Sudoku-Example are already present different complexity level of problem:
    easy , medium  -> solvable just thanks the known criteria of Sudoku
    hard , extreme -> solvable with criteria + randomly completion of the matrix
"""

from enum import Enum
from copy import deepcopy
SIZE = 9


class State(Enum):
    """
    Create an enumerate list for the possible situation in a cell of the sudoku
        VALID   -> the number can be inserted
        INVALID -> the number cannot be inserted
        SET     -> the number is been inserted
        OCCUPIED-> to indicate in a cell there is an other number
    """
    VALID = 0
    INVALID = 1
    SET = 2
    OCCUPIED = 3


class SudokuHandler:
    def __init__(self):
        """
        Initialize the structures
        """
        self.size = SIZE  # 9x9 sudoku
        self.matrix = []  # This matrix will contain the numbers
        self.grid = []    # This is a set of matrix (one for each number) of value in State
        # Initialize the grid of matrices (one for each number)
        for _ in range(0 , self.size):
            self.grid.append(self.initMask())
        self.openList = []  # The openList to be use in case of randomly solution
        self.closedList = []
        self.randomSearch = False

    def initMask(self):
        """
        Method that initialize the generic matrix board to all VALID values
        :return: the new matrix initialized
        """
        # Initialize the matrix
        matrix = []
        for i in range(0 , self.size):
            row = []
            for j in range(0 , self.size):
                # Set the VALID state in every cell
                row.append(State.VALID)
            matrix.append(row)
        return matrix

    def readMatrix(self):
        """
        Method used to read from a file the sudoku starting configuration (initializing self.matrix)
            and initialize self.grid
        """
        # Open the file to read the sudoku game
        with open("Sudoku-Example/Sudoku-Hard.txt") as f:
            for _ in range(0 , self.size):
                rowRead = f.readline().split(" ")
                row = []
                for num in rowRead:
                    row.append(num.rstrip('\n'))  # To avoid '\n' at the end
                self.matrix.append(row)
        # Close the file
        f.close()
        # Create the initial grid
        self.updateGrid()

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
        Method that print the mask matrices (print the whole self.grid)
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
        Method that checks if the matrix is full and completely -> if the Sudoku is solved
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

    def takeSquare(self, x, y):
        """
        Given the coordinate x , y return the first index of the sub-matrix in which the element (x , y) belongs
        :param x: is the x coordinate
        :param y: is the y coordinate
        :return: a tuple of coordinates
        """
        x2, y2 = 0, 0

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

        return x2, y2

    def updateGrid(self , x = None , y = None):
        """
        Method that updates the grid after a number is been inserted
            (or as init of the grid during the first phase -> x , y not specified)
        :param x: is the coordinate x of the new number
        :param y: is the coordinate y of the new number
        """
        # If it's the first call
        if x is None and y is None:
            if self.randomSearch:
                # Initialize the grid of matrices for the case of coming back to a matrix with less numbers
                self.grid = []
                for _ in range(0, self.size):
                    self.grid.append(self.initMask())
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

            # Notify the row/column that they are invalid in the mask corresponding the number inserted
            for i in range(0 , self.size):
                if (self.grid[numberInserted])[x][i] != State.OCCUPIED and \
                        (self.grid[numberInserted])[x][i] != State.SET:
                    (self.grid[numberInserted])[x][i] = State.INVALID
                if (self.grid[numberInserted])[i][y] != State.OCCUPIED and \
                        (self.grid[numberInserted])[i][y] != State.SET:
                    (self.grid[numberInserted])[i][y] = State.INVALID

            # Notify the whole sub-square that it is invalid in the mask corresponding the number inserted
            # Take the coordinate of the first cell in high-left of the sub-matrix
            x2 , y2 = self.takeSquare(x, y)

            for iRow in range(x2 , x2 + 3): # from x2 to x2 + 2 (x2 + 3 is excluded)
                for iCol in range(y2 , y2 + 3):
                    if (self.grid[numberInserted])[iRow][iCol] != State.OCCUPIED and \
                            (self.grid[numberInserted])[iRow][iCol] != State.SET:
                        (self.grid[numberInserted])[iRow][iCol] = State.INVALID

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
                    if (self.grid[m - 1])[i][j] == State.VALID and not self.isPresentInArray(m , i):
                        validPosition += 1
                # If there is just one position valid -> insert the m number in that position
                if validPosition == 1:
                    for j in range(0, self.size):
                        if (self.grid[m - 1])[i][j] == State.VALID:
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
                    if (self.grid[m - 1])[j][i] == State.VALID and not self.isPresentInArray(m , i , False):
                        validPosition += 1
                # If there is just one position valid -> insert the m number in that position
                if validPosition == 1:
                    for j in range(0, self.size):
                        if (self.grid[m - 1])[j][i] == State.VALID:
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
                            if (self.grid[m - 1])[i + i2][j + j2] == State.VALID \
                                    and not self.isPresentInSquare(m , i , j):
                                validPosition += 1
                    # If there is just one position valid -> insert the m number in that position
                    if validPosition == 1:
                        for i2 in range(0, 3):
                            for j2 in range(0, 3):
                                if (self.grid[m - 1])[i + i2][j + j2] == State.VALID:
                                    x = i + i2
                                    y = j + j2
                        print("S: inserted " + str(m) + " in position " + str(x) + "," + str(y))
                        self.matrix[x][y] = str(m)
                        # Update the grid
                        self.updateGrid(x , y)
                        return True

        # If nothing has been added
        return False

    def getNumberToInsert2(self):
        """
        Method that find the number with more VALID state
        :return: return the number chose
        """
        minValues = []
        minCount = self.size * self.size
        numberChose = 1
        for num in range(1 , self.size + 1):
            numCount = 0
            for i in range(0 , self.size):
                for j in range(0 , self.size):
                    if self.grid[num - 1][i][j] == State.VALID:
                        numCount += 1
            minValues.append(numCount)
            if 0 < numCount < minCount:
                minCount = numCount
                numberChose = num
        print(minValues)
        return numberChose

    def getNumberToInsert(self):
        """
        Method that find the number more inserted
        :return: return the number chose
        """
        maxCount = 0
        numberChose = 1
        for num in range(1 , self.size + 1):
            numCount = 0
            for i in range(0 , self.size):
                for j in range(0 , self.size):
                    if self.matrix[i][j] == str(num):
                        numCount += 1
            if 9 > numCount > maxCount:
                maxCount = numCount
                numberChose = num
        return numberChose

    def insertInOpenList(self , matrix):
        """
        Method that add the current configuration in the openList only if it's not already in there or if it's not
            an already visited node (if it is in the closed list)
        :param matrix: is the configuration to add
        """
        for node in self.openList:
            if node == matrix:
                return
        for node in self.closedList:
            if node == matrix:
                return
        self.openList.append(matrix)

    def expand(self , number):
        """
        Method that insert a number in a possible position in the matrix
        :param number: is the number to be inserted
        """
        # For each VALID position generate a child and insert it into the openList
        for i in range(0 , self.size):
            for j in range(0 , self.size):
                if self.grid[number - 1][i][j] == State.VALID:
                    # Insert the number in a copy
                    mtr = deepcopy(self.matrix)
                    mtr[i][j] = str(number)
                    # Put the new list in the open list if it's not already present
                    self.insertInOpenList(mtr)

    def randomlySolver(self):
        """
        When it's not possible to solve the sudoku following a logical criteria this method is called
        Method that according to the grid/matrix of the current configuration try to insert numbers
        It will use an open list (the frontier) that contains the node to be expanded
        it will use a closed list that contains the node already expanded
        It will be use a depth-search strategy -> there are not infinite path
        The element will be put at the end of the openList and , at the next step, the node chosen will be
            the one in the last position (depth-search strategy starting from the right)
        :return: the solved matrix
        """
        self.openList = []

        print("Computing the randomly research...")

        # Take the number more inserted -> less probability to do a wrong insertion
        numberToBeInserted = self.getNumberToInsert()

        # Insert the number chose in all the possible cells and create a child for each possibility
        #   (insert the child in the open list)
        self.expand(numberToBeInserted)

        # Until when there is at least one element in the list to be expanded
        i = 1
        while len(self.openList) > 0:
            i += 1

            # Take the last element -> the insertion is more efficient instead of insertion in the 0 position
            self.matrix = self.openList[len(self.openList) - 1]
            # Delete the node just extracted from the openList (the last element)
            del self.openList[len(self.openList) - 1]

            if self.isCompleted():
                print("The computation ended correctly")
                self.printMatrix()
                print("Result of the computation:")
                print("Total number of iterations: " + str(i))
                print("The size of the openList is " + str(len(self.openList)))
                print("The size of the closedList is " + str(len(self.closedList)))
                return
            # Generate the new grid
            self.updateGrid()
            # Take the new number to insert
            numberToBeInserted = self.getNumberToInsert()
            # Expand the current matrix
            self.expand(numberToBeInserted)
            # Add the element in the closed list
            self.closedList.append(self.matrix)

        print("Impossible to find a solution")

    def process(self):
        """
        This is the main function that handler the algorithm
        """
        # Read the game
        self.readMatrix()
        # Update the masks
        self.updateGrid()
        self.printMatrix()

        while not self.isCompleted():
            # Insert a number
            result = self.insertANumber()
            if not result:
                print("It's not possible to find a solution with logic criteria")
                self.randomSearch = True
                self.randomlySolver()

                return
            # Show the new matrices
            self.printMatrix()
        print("The computation ended correctly")


if __name__ == "__main__":
    sudokuHandler = SudokuHandler()
    sudokuHandler.process()



