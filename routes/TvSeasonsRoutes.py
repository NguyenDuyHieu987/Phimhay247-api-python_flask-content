from flask import *
from flask_cors import cross_origin
import configs
from controllers.TvSeasonsControllers import TVSeason


def tv_seasons_routes(app, cache):
    tvseason = TVSeason()

    @app.route("/tv/<id>/season/<season_number>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def tv_seasons_route(id, season_number):
        return tvseason.tv_seasons(id, season_number)
