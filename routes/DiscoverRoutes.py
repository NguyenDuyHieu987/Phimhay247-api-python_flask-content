from flask import *
from flask_cors import cross_origin
import configs
from controllers.DiscoverControllers import Discover


def discover_routes(app, cache):
    discover = Discover()

    @app.route("/discover/<type>", methods=["GET"])
    @cache.cached()
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def discover_route(type):
        return discover.discover(type)
