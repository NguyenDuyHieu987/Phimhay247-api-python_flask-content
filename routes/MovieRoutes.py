from flask import *

# from flask_cors import cross_origin
import configs
from controllers.MovieControllers import Movie


def movie_routes(app, cache):
    prefix_route = "movie"

    movie = Movie()
    ## Detail movie

    @app.route(f"/{prefix_route}/detail/<id>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    # @cache.cached()
    def get_movie_route(id):
        return movie.get(id)

    ## Add movie

    @app.route(f"/{prefix_route}/add", methods=["POST"])
    # @cross_origin(origins=configs.API_ADMIN_ORIGINS_CONFIG)
    def add_movie_route():
        return movie.add()

    ## Edit movie

    @app.route(f"/{prefix_route}/edit/<id>", methods=["POST"])
    # @cross_origin(origins=configs.API_ADMIN_ORIGINS_CONFIG)
    def edit_movie_route(id):
        return movie.edit(id)

    ## Update view movie

    @app.route(f"/{prefix_route}/updateview/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def update_view_movie_route(id):
        return movie.update_view(id)
