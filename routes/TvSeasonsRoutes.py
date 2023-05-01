from flask import *
from flask_cors import cross_origin
import configs


def tv_seasons_routes(app):
    from controllers.TvSeasonsControllers import tv_seasons

    @app.route("/tv/<id>/season/<season_number>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def tv_seasons_route(id, season_number):
        return tv_seasons(id, season_number)
