from flask import *
from flask_cors import cross_origin
import configs


def search_routes(app):
    from controllers.SearchControllers import search

    @app.route("/search/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_route(type):
        return search(type)
