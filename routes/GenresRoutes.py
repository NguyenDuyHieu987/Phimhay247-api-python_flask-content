from flask import *
from flask_cors import cross_origin
import configs


def genres_routes(app):
    from controllers.GenresControllers import genres

    @app.route("/genre/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def genres_route(type):
        return genres(type)
