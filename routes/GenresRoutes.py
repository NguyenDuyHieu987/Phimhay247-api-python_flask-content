from flask import *
from flask_cors import cross_origin
import configs
from controllers.GenresControllers import Genre


def genres_routes(app, cache):
    genre = Genre()

    @app.route("/genre/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def genres_route(type):
        return genre.genres(type)
