from flask import *


def discover_routes(app):
    from controllers.DiscoverControllers import discover

    @app.route("/discover/<type>", methods=["GET"])
    def discover_route(type):
        return discover(type)
