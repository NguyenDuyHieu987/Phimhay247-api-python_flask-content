from flask import *
from flask_cors import cross_origin
import configs
from controllers.RecommendControllers import Recommend


def recommend_routes(app, cache):
    recomment = Recommend()

    @cache.cached(timeout=3600)
    @app.route("/recommend/<userid>/getrecommend", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def recommend_route(userid):
        return recomment.get_recommend(userid)
