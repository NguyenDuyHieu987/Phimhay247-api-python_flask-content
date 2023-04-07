from flask import *


def movie_slug_routes(app):
    from controllers.MovieSlugControllers import movie_slug

    @app.route("/movie/<slug>", methods=["GET"])
    def movie_slug_route(slug):
        return movie_slug(slug)
