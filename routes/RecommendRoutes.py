from flask import *
from flask_cors import cross_origin
import configs
from controllers.RecommendControllers import Recommend


def recommend_routes(app, cache):
    recomment = Recommend()

    @app.route("/recommend/getrecommend", methods=["GET"])
    @cache.cached()
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def recommend_route():
        return recomment.get_recommend()
