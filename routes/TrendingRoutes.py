from flask import *
from flask_cors import cross_origin
import configs
from controllers.TrendingControllers import Trend


def trending_routes(app, cache):
    trend = Trend()

    @cache.cached(timeout=3600)
    @app.route("/trending/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def trending_route(type):
        return trend.trending(type)
