from flask import *
from flask_cors import cross_origin
import configs
from controllers.CountriesControllers import Country


def countries_routes(app):
    country = Country()

    @app.route("/country/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def countries_route(type):
        return country.countries(type)
