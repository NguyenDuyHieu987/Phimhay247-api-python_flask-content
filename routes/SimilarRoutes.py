from flask import *
from flask_cors import cross_origin
import configs


def similar_routes(app):
    from controllers.SimilarControllers import get_similar

    @app.route("/similar/<type>/<movieid>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def similar_route(type, movieid):
        return get_similar(type, movieid)
