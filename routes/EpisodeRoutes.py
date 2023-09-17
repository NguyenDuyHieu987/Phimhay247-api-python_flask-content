from flask import *
# from flask_cors import cross_origin
import configs
from controllers.EpisodeControllers import Episode


def episode_routes(app, cache):
    episode = Episode()

    @app.route("/episode/list/<movieId>/<seasonId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_list_episodes_route(movieId, seasonId):
        return episode.getList(movieId, seasonId)

    @app.route("/episode/get/<movieId>/<seasonId>/<episodeNumber>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_episode_route(movieId, seasonId, episodeNumber):
        return episode.get(movieId, seasonId, episodeNumber)
