from flask import *

# from flask_cors import cross_origin
import configs
from controllers.MovieSlugControllers import MovieSlug


def movie_slug_routes(app, cache):
    prefix_route = "movie"

    movieslug = MovieSlug()

    @app.route(f"/{prefix_route}/<slug>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached(query_string=True)
    def get_slug_movie_slug_route(slug):
        return movieslug.get_slug(slug)

    @app.route(f"/{prefix_route}/discover/<slug>", methods=["GET"])
    @cache.cached(query_string=True)
    def filter_movie_slug_route(slug):
        return movieslug.filter(slug)
