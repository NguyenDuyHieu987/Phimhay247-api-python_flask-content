from flask import *

# from flask_cors import cross_origin
import configs
from controllers.TrendingControllers import Trending


def trending_routes(app, cache):
    prefix_route = "trending"

    trending = Trending()

    @app.route(f"/{prefix_route}/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached(query_string=True)
    def get_slug_trending_route(type):
        return trending.get_slug(type)
