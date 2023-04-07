from flask import *


def movie_routes(app):
    ## Detail movie
    from controllers.MovieControllers import detail_movie

    @app.route("/movie/detail/<id>", methods=["GET"])
    def detail_movie_route(id):
        return detail_movie(id)

    ## Edit movie
    from controllers.MovieControllers import edit_movie

    @app.route("/movie/edit/<id>", methods=["POST"])
    def edit_movie_route(id):
        return edit_movie(id)

    ## Update view movie
    from controllers.MovieControllers import update_view_movie

    @app.route("/movie/updateview/<id>", methods=["POST"])
    def update_view_movie_route(id):
        return update_view_movie(id)
