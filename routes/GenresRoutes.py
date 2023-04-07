from flask import *


def genres_routes(app):
    from controllers.GenresControllers import genres

    @app.route("/genre/<type>", methods=["GET"])
    def genres_route(type):
        return genres(type)
