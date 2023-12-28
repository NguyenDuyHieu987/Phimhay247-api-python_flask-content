from flask import *

# from flask_cors import cross_origin
import configs
from controllers.EpisodeControllers import Episode


def episode_routes(app, cache):
    prefix_route = "episode"

    episode = Episode()

    @app.route(f"/{prefix_route}/list/<movieId>/<seasonId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_list_episode_route(movieId, seasonId):
        return episode.get_list(movieId, seasonId)

    @app.route(
        f"/{prefix_route}/get/<movieId>/<seasonId>/<episodeNumber>", methods=["GET"]
    )
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_episode_route(movieId, seasonId, episodeNumber):
        return episode.get(movieId, seasonId, episodeNumber)
