from flask import *
# from flask_cors import cross_origin
import configs
from controllers.SortByControllers import Sortby


def sortbys_routes(app, cache):
    sortby = Sortby()

    @app.route("/sortby/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def sortbys_route(type):
        return sortby.sortby(type)
