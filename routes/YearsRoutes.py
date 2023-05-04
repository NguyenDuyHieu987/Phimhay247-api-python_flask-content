from flask import *
from flask_cors import cross_origin
import configs
from controllers.YearsControllers import Year


def years_routes(app):
    year = Year()

    @app.route("/year/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def years_route(type):
        return year.years(type)
