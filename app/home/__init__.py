from flask import Blueprint


home = Blueprint(
    "home",
    __name__,
    static_folder="static",
    static_url_path="/home/static",
    template_folder="templates",
    url_prefix="/"
)


from . import views