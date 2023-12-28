from flask import *

# from flask_cors import cross_origin
import configs
from controllers.CountriesControllers import Country


def countries_routes(app, cache):
    prefix_route = "country"

    country = Country()

    @app.route(f"/{prefix_route}/get-all", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_all_countries_route(type):
        return country.get_all(type)
