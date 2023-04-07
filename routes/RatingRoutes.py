from flask import *


def rating_routes(app):
    from controllers.RatingControllers import rating_movie_tv

    @app.route("/<type>/rating/<id>", methods=["POST"])
    def rating_route(type, id):
        return rating_movie_tv(type, id)
