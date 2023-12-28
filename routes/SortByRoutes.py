from flask import *

# from flask_cors import cross_origin
import configs
from controllers.SortByControllers import Sortby


def sortbys_routes(app, cache):
    prefix_route = "sortby"

    sortby = Sortby()

    @app.route(f"/{prefix_route}/get-all", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_all_sortbys_route(type):
        return sortby.get_all(type)
