#==================================================================================================
# Imports
#==================================================================================================
# Third Party
from flask import jsonify, request, render_template

# Application
from . import sudoku_solver
from app.sudoku_solver import sudoku_app


#==================================================================================================
# Global Variables
#==================================================================================================
sudoku = sudoku_app.SudokuApp()


#==================================================================================================
# Routes
#==================================================================================================
@sudoku_solver.route("/", methods=["GET"])
def main_page():
    return render_template("sudoku_solver/index.html")


@sudoku_solver.route("/table", methods=["POST"])
def post_table():
    # Prepare Variables
    values = dict(request.get_json())

    # Set Table
    sudoku.add_request(values)

    # Prepare Response
    response = {
        "message": "Table Received successfully.",
    }

    # Return Response
    return jsonify(response), 200


@sudoku_solver.route("/table/<reqId>", methods=["GET"])
def get_table(reqId):
    # Prepare Variables
    req = sudoku.get_request(int(reqId))

    # Prepare Response
    response = {
        sudoku_app.KEY_TABLE: req[sudoku_app.KEY_TABLE],
        sudoku_app.KEY_REQ_ID: req[sudoku_app.KEY_REQ_ID],
        sudoku_app.KEY_MSG: req[sudoku_app. KEY_MSG]
    }

    # Return Response
    return jsonify(response), 200
