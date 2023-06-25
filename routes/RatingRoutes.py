from flask import *
from flask_cors import cross_origin
import configs
from controllers.RatingControllers import Rate


def rating_routes(app):
    rate = Rate()

    @app.route("/rating/get/<type>/<id>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_rating_route(type, id):
        return rate.get_rating(type, id)

    @app.route("/rating/<type>/<id>", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def rating_route(type, id):
        return rate.rating(type, id)
