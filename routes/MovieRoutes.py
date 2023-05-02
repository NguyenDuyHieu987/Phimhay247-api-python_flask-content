from flask import *
from flask_cors import cross_origin
import configs


def movie_routes(app, cache):
    ## Detail movie
    from controllers.MovieControllers import detail_movie

    @cache.cached(timeout=3000)
    @app.route("/movie/detail/<id>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def detail_movie_route(id):
        return detail_movie(id)

    ## Add movie
    from controllers.MovieControllers import add_movie

    @app.route("/movie/add", methods=["POST"])
    @cross_origin(origins=configs.API_ADMIN_ORIGINS_CONFIG)
    def add_movie_route():
        return add_movie()

    ## Edit movie
    from controllers.MovieControllers import edit_movie

    @app.route("/movie/edit/<id>", methods=["POST"])
    @cross_origin(origins=configs.API_ADMIN_ORIGINS_CONFIG)
    def edit_movie_route(id):
        return edit_movie(id)

    ## Update view movie
    from controllers.MovieControllers import update_view_movie

    @app.route("/movie/updateview/<id>", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def update_view_movie_route(id):
        return update_view_movie(id)
