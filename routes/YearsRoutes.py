from flask import *

# from flask_cors import cross_origin
import configs
from controllers.YearsControllers import Year


def years_routes(app, cache):
    prefix_route = "year"

    year = Year()

    @app.route(f"/{prefix_route}/get-all", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_all_years_route(type):
        return year.get_all(type)
