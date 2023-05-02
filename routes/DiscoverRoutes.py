from flask import *
from flask_cors import cross_origin
import configs


def discover_routes(app, cache):
    from controllers.DiscoverControllers import discover

    @cache.cached(timeout=3600)
    @app.route("/discover/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def discover_route(type):
        return discover(type)
