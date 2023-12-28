from flask import *

# from flask_cors import cross_origin
import configs
from controllers.RecommendControllers import Recommend


def recommend_routes(app, cache):
    prefix_route = "recommend"

    recomment = Recommend()

    @app.route(f"/{prefix_route}/get-all", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    # @cache.cached(query_string=True)
    def get_all_recommend_route():
        return recomment.get_all()
