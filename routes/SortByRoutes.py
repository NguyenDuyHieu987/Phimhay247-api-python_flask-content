from flask import *
from flask_cors import cross_origin
import configs


def sortbys_routes(app):
    from controllers.SortByControllers import sortby

    @app.route("/sortby/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def sortbys_route(type):
        return sortby(type)
