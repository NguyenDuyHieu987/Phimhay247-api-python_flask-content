from flask import *


def similar_routes(app):
    from controllers.SimilarControllers import get_similar

    @app.route("/similar/<type>/<movieid>", methods=["GET"])
    def similar_route(type, movieid):
        return get_similar(type, movieid)
