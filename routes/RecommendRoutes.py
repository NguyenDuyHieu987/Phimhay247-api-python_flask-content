from flask import *
from flask_cors import cross_origin
import configs


def recommend_routes(app, cache):
    from controllers.RecommendControllers import get_recommend

    @cache.cached(timeout=3600)
    @app.route("/recommend/<userid>/getrecommend", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def recommend_route(userid):
        return get_recommend(userid)
