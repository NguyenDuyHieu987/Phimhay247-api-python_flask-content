from flask import *


def recommend_routes(app):
    from controllers.RecommendControllers import get_recommend

    @app.route("/recommend/<userid>/getrecommend", methods=["GET"])
    def recommend_route(userid):
        return get_recommend(userid)
