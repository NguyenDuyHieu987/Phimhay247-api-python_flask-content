from flask import *


def search_routes(app):
    from controllers.SearchControllers import search

    @app.route("/search/<type>", methods=["GET"])
    def search_route(type):
        return search(type)
