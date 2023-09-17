from flask import *
# from flask_cors import cross_origin
import configs
from controllers.TrendingControllers import Trending


def trending_routes(app, cache):
    trending = Trending()

    @app.route("/trending/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached(query_string=True)
    def trending_route(type):
        return trending.get_trending(type)
