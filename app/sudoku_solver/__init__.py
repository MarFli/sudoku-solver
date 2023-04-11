from flask import Blueprint


sudoku_solver = Blueprint(
    "sudoku_solver",
    __name__,
    static_folder="static",
    static_url_path="/sudoku_solver/static",
    template_folder="templates",
    url_prefix="/sudoku-solver"
)


from . import views