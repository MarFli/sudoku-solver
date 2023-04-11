#==================================================================================================
# Imports
#==================================================================================================
# Standard Library
from threading import Lock

# Application
from app.sudoku_solver.sudoku import Sudoku


#==================================================================================================
# Constants
#==================================================================================================
KEY_TABLE = "table"
KEY_REQ_ID = "reqId"
KEY_MSG = "msg"


#==================================================================================================
# Classes
#==================================================================================================
class SudokuApp():
    def __init__(self, timeout_lim: int = 10) -> None:
        self.__sud = Sudoku(timeout_lim)
        self.__requests = []
        self.__lock = Lock()


    #--------------------------
    # Public Functions
    #--------------------------
    def add_request(self, req: dict) -> None:
        self.__lock.acquire()
        self.__requests.append(req)
        self.__lock.release()


    def get_request(self, id: int) -> dict:
        self.__lock.acquire()

        # Prepare Variavbles
        table = None
        msg = ""
        is_solved = False

        # Get Request
        for i in range(len(self.__requests)):
            if (self.__requests[i][KEY_REQ_ID] == id):
                # Set table
                self.__sud.set_table(self.__requests[i][KEY_TABLE])

                # Solve
                is_solved, msg = self.__sud.solve()
                if is_solved:
                    table = self.__sud.get_table()

                # Remove dict from array
                self.__requests.pop(i)

                break

        req = { KEY_TABLE: table, KEY_REQ_ID: id, KEY_MSG: msg }

        self.__lock.release()

        return req
