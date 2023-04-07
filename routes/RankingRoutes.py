from flask import *


def ranking_routes(app):
    from controllers.RankingControllers import ranking

    @app.route("/ranking/<slug>", methods=["GET"])
    def ranking_route(slug):
        return ranking(slug)
