from flask import *


def trending_routes(app):
    from controllers.TrendingControllers import trending

    @app.route("/trending/<type>", methods=["GET"])
    def trending_route(type):
        return trending(type)
