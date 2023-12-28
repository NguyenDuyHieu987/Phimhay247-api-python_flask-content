from flask import *

# from flask_cors import cross_origin
import configs
from controllers.GenresControllers import Genre


def genres_routes(app, cache):
    prefix_route = "genre"

    genre = Genre()

    @app.route(f"/{prefix_route}/get-all", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_all_genres_route(type):
        return genre.get_all(type)
