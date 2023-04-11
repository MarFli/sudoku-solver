#==================================================================================================
# Imports
#==================================================================================================
# Standard Library
import time


#==================================================================================================
# Classes
#==================================================================================================
class Sudoku:
    def __init__(self, timeout_lim: int = 10) -> None:
        self.__table = [[0 for i in range(9)] for j in range(9)]  # MF: Creates 9x9 table
        self.__timeout_lim = timeout_lim
        self.__start_timer = 0


    #--------------------------
    # Private Functions
    #--------------------------
    def __find_empty_location(self, l: list) -> bool:
        for row in range(9):
            for col in range(9):
                if (self.__table[row][col]== 0):
                    l[0]= row
                    l[1]= col
                    return True

        return False


    def __used_in_row(self, row: int, num: int) -> bool:
        for i in range(9):
            if (self.__table[row][i] == num):
                return True

        return False


    def __used_in_col(self, col: int, num: int) -> bool:
        for i in range(9):
            if (self.__table[i][col] == num):
                return True

        return False


    def __used_in_box(self, row: int, col: int, num: int) -> bool:
        for i in range(3):
            for j in range(3):
                if (self.__table[i + row][j + col] == num):
                    return True

        return False


    def __is_location_safe(self, row: int, col: int, num: int) -> bool:
        # Check if 'num' is not already placed in current row, current column and current 3x3 box
        return  (not self.__used_in_row(row, num) and (not self.__used_in_col(col, num) and
                (not self.__used_in_box(row - (row % 3), col - (col % 3), num))))


    def __is_table_empry(self) -> bool:
        for i in range(9):
            for j in range(9):
                if (self.__table[i][j] != 0):
                    return False

        return True


    def __is_duplicate_arr(self, arr: list) -> bool:
        # Remove all 0 from arr
        new_arr = [i for i in arr if i != 0]

        # Check if duplicates in arr
        if len(new_arr) == len(set(new_arr)):
            return False
        else:
            return True


    def __get_box_arr(self, box_index) -> list:
        # Prepare variables
        row = box_index - (box_index % 3)
        col = (box_index % 3) * 3
        arr = []

        # Get values
        for i in range(3):
            for j in range(3):
                arr.append(self.__table[i + (row - (row % 3))][j + (col - (col % 3))])

        return arr [:]


    def __is_duplicate_table(self) -> tuple:
        for i in range(9):
            # Check Row
            if self.__is_duplicate_arr(self.__table[i]):
                return (True, "Duplicate in a row " + str(i + 1))

            # Check Col
            if self.__is_duplicate_arr([self.__table[j][i] for j in range(9)]):
                return (True, "Duplicate in a column " + str(i + 1))

            # Check Box
            if self.__is_duplicate_arr(self.__get_box_arr(i)):
                return (True, "Duplicate in a box " + str(i + 1))

        return (False, "")


    def __solve_alg(self) -> bool:
        # Check Timeout
        if (time.time() > (self.__start_timer + self.__timeout_lim)):
            return False

        # 'l' is a list variable that keeps the record of row and col in find_empty_location Function
        l = [0, 0]

        # If there is no unassigned location, we are done
        if (not self.__find_empty_location(l)):
            return True

        # Assigning list values to row and col that we got from the above Function
        row = l[0]
        col = l[1]

        # Consider digits 1 to 9
        for num in range(1, 10):
            # If looks promising
            if (self.__is_location_safe(row, col, num)):
                # Make tentative assignment
                self.__table[row][col]= num

                # Return, if success
                if (self.__solve_alg()):
                    return True

                # Failure, unmake & try again
                self.__table[row][col] = 0

        # This triggers backtracking
        return False


    #--------------------------
    # Public Functions
    #--------------------------
    def set_num(self, row: int, col: int, num: int) -> None:
        self.__table[row][col] = num


    def set_table(self, table: list) -> None:
        self.__table = table


    def get_num(self, row: int, col: int) -> int:
        return self.__table[row][col]


    def get_table(self) -> list:
        return self.__table [:]


    def solve(self) -> tuple:
        # Check if empry arr
        if self.__is_table_empry():
            return (False, "Table is empty")

        # Check if duplicates
        is_duplicate, duplicate_msg = self.__is_duplicate_table()
        if is_duplicate:
            return (False, duplicate_msg)

        # Check if only one solution
        # TODO

        # Solve Sudoku
        self.__start_timer = time.time()
        if self.__solve_alg():
            return (True, "Solved")
        elif (time.time() > (self.__start_timer + self.__timeout_lim)):     # MF: Timeout
            return (False, "Cannot find solution")
        else:
            return (False, "No solution")
