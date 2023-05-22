from flask import *
from flask_cors import cross_origin
import configs
from controllers.RatingControllers import Rate


def rating_routes(app):
    rate = Rate()

    @app.route("/rating/<type>/<id>", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def rating_route(type, id):
        return rate.rating_movie_tv(type, id)
