from flask import *
from flask_cors import cross_origin
import configs


def rating_routes(app):
    from controllers.RatingControllers import rating_movie_tv

    @app.route("/rating/<type>//<id>", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def rating_route(type, id):
        return rating_movie_tv(type, id)
