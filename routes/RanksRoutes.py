from flask import *

# from flask_cors import cross_origin
import configs
from controllers.RanksControllers import Rank


def ranking_routes(app, cache):
    rank = Rank()

    @app.route("/ranks/<slug>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def ranking_route(slug):
        return rank.ranking(slug)
