from flask import *
from flask_cors import cross_origin
import configs


def ranking_routes(app, cache):
    from controllers.RankingControllers import ranking

    @cache.cached(timeout=3600)
    @app.route("/ranking/<slug>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def ranking_route(slug):
        return ranking(slug)
