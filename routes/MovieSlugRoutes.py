from flask import *
from flask_cors import cross_origin
import configs
from controllers.MovieSlugControllers import MovieSlug


def movie_slug_routes(app, cache):
    movieslug = MovieSlug()

    @app.route("/movie/<slug>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def movie_slug_route(slug):
        return movieslug.movie_slug(slug)
