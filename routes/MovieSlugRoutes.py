from flask import *
from flask_cors import cross_origin
import configs


def movie_slug_routes(app):
    from controllers.MovieSlugControllers import movie_slug

    @app.route("/movie/<slug>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def movie_slug_route(slug):
        return movie_slug(slug)
