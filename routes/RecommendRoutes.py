from flask import *
from flask_cors import cross_origin
import configs


def recommend_routes(app):
    from controllers.RecommendControllers import get_recommend

    @app.route("/recommend/<userid>/getrecommend", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def recommend_route(userid):
        return get_recommend(userid)
