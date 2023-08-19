from flask import *
from flask_cors import cross_origin
import configs
from controllers.DiscoverControllers import Discover


def discover_routes(app, cache):
    discover = Discover()

    @app.route("/discover/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached(query_string=True)
    def discover_route(type):
        return discover.discover(type)
