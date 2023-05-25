from flask import *
from flask_cors import cross_origin
import configs
from controllers.CountriesControllers import Country


def countries_routes(app, cache):
    country = Country()

    @app.route("/country/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def countries_route(type):
        return country.countries(type)
