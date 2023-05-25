from flask import *
from flask_cors import cross_origin
import configs
from controllers.RankingControllers import Rank


def ranking_routes(app, cache):
    rank = Rank()

    @app.route("/ranking/<slug>", methods=["GET"])
    @cache.cached(timeout=3600)
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def ranking_route(slug):
        return rank.ranking(slug)
