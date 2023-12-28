from flask import *

# from flask_cors import cross_origin
import configs
from controllers.SimilarControllers import Similar


def similar_routes(app, cache):
    prefix_route = "similar"

    similar = Similar()

    @app.route(f"/{prefix_route}/<type>/<movieid>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_slug_similar_route(type, movieid):
        return similar.get_slug(type, movieid)
