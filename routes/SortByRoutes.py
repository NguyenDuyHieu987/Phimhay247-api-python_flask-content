from flask import *


def sortbys_routes(app):
    from controllers.SortByControllers import sortby

    @app.route("/sortby/<type>", methods=["GET"])
    def sortbys_route(type):
        return sortby(type)
