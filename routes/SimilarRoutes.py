from flask import *
from flask_cors import cross_origin
import configs
from controllers.SimilarControllers import Similar


def similar_routes(app, cache):
    similar = Similar()

    @app.route("/similar/<type>/<movieid>", methods=["GET"])
    @cache.cached(timeout=3600)
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def similar_route(type, movieid):
        return similar.get_similar(type, movieid)
