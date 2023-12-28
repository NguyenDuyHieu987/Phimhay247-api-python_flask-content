from flask import *

# from flask_cors import cross_origin
import configs
from controllers.DiscoverControllers import Discover


def discover_routes(app, cache):
    prefix_route = "discover"

    discover = Discover()

    @app.route(f"/{prefix_route}/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached(query_string=True)
    def get_slug_discover_route(type):
        return discover.get_slug(type)
