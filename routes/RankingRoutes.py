from flask import *
from flask_cors import cross_origin
import configs


def ranking_routes(app):
    from controllers.RankingControllers import ranking

    @app.route("/ranking/<slug>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def ranking_route(slug):
        return ranking(slug)
