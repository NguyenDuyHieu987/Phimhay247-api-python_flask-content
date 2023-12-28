from flask import *

# from flask_cors import cross_origin
import configs
from controllers.RatingControllers import Rate


def rating_routes(app):
    prefix_route = "rating"

    rate = Rate()

    @app.route(f"/{prefix_route}/get/<type>/<id>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_rating_route(type, id):
        return rate.get(type, id)

    @app.route(f"/{prefix_route}/<type>/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def rate_rating_route(type, id):
        return rate.rate(type, id)
