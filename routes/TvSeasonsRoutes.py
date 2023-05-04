from flask import *
from flask_cors import cross_origin
import configs
from controllers.TvSeasonsControllers import TVSeason


def tv_seasons_routes(app, cache):
    tvseason = TVSeason()

    @cache.cached(timeout=3600)
    @app.route("/tv/<id>/season/<season_number>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def tv_seasons_route(id, season_number):
        return tvseason.tv_seasons(id, season_number)
