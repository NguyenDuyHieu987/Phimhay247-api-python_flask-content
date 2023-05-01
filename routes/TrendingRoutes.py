from flask import *
from flask_cors import cross_origin
import configs


def trending_routes(app):
    from controllers.TrendingControllers import trending

    @app.route("/trending/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def trending_route(type):
        return trending(type)
