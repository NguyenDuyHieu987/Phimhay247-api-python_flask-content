from flask import *


def tv_seasons_routes(app):
    from controllers.TvSeasonsControllers import tv_seasons

    @app.route("/tv/<id>/season/<season_number>", methods=["GET"])
    def tv_seasons_route(id, season_number):
        return tv_seasons(id, season_number)
