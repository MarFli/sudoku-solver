#==================================================================================================
# Imports
#==================================================================================================
# Third Party
from flask import Flask

# Application
from app.home import home
from app.sudoku_solver import sudoku_solver


#==================================================================================================
# App
#==================================================================================================
def create_app() -> Flask:
    # Create app
    app = Flask(__name__)

    # Configure app
    app.config.from_object("config.ProductionConfig")

    # Register all Blueprints
    app.register_blueprint(home)
    app.register_blueprint(sudoku_solver)

    # Return app
    return app
