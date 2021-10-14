# Sudoku-Solver
Date: 14/10/2021

Author: Matteo Nunziante

Structures used:
- matrix: the configuration of the sudoku
- grid: a list of 9 matrices, one for each number, made by State element to 
 say if a number can go in a position or not

If it's impossible to solve the puzzle with the known criteria, the algorithm will try to fill it
randomly, inserting the number that:
- have the highest number of VALID positions (low level of efficiency)
- have the highest number of element inserted (high level of efficiency)

Furthermore, in that case other two structures are used:
- openList: to keep the configuration to be expanded (expanding = add a random number where it's possible)
- closedList: to keep trace of all the numbers already expanded (to avoid repetition/cycle)

To run the algorithm insert the sudoku in a text file (for example in the directory "Sudoku-Example") and modify
    the method readMatrix with the right path

Example:

                              Sudoku format in the txt file:
                                    _ _ 7 6 _ _ 2 9 4
                                    _ _ _ 7 _ _ _ _ 3
                                    _ _ 6 9 _ 4 _ _ _
                                    _ _ 1 _ _ _ _ _ 2
                                    9 _ 4 2 _ _ 8 _ 5
                                    7 2 3 _ 8 5 _ _ 6
                                    _ 3 9 _ 1 _ _ _ _
                                    1 _ _ 8 6 _ _ _ _
                                    6 7 8 3 _ 2 _ _ _

In the directory Sudoku-Example are already present different complexity level of problems:
- easy , medium  -> solvable just thanks the known criteria of Sudoku
- hard , extreme -> solvable with criteria + randomly completion of the matrix