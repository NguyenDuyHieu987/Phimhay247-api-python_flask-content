from flask import *

# from flask_cors import cross_origin
import configs
from controllers.SeasonsControllers import Season


def seasons_routes(app, cache):
    prefix_route = "season"

    season = Season()

    @app.route(f"/{prefix_route}/list/<seriesId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_list_seasons_route(seriesId):
        return season.get_list(seriesId)

    @app.route(f"/{prefix_route}/get/<movieId>/<seasonId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_season_route(movieId, seasonId):
        return season.get(movieId, seasonId)
