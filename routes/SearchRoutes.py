from flask import *
from flask_cors import cross_origin
import configs
from controllers.SearchControllers import Search


def search_routes(app, cache):
    search = Search()

    @cache.cached(timeout=3600)
    @app.route("/search/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_route(type):
        return search.search(type)
