from flask import *
from flask_cors import cross_origin
import configs


def countries_routes(app):
    from controllers.CountriesControllers import countries

    @app.route("/country/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def countries_route(type):
        return countries(type)
