from flask import *


def tv_routes(app):
    ## Detail Tv
    from controllers.TvControllers import detail_tv

    @app.route("/tv/detail/<id>", methods=["GET"])
    def detail_tv_route(id):
        return detail_tv(id)

    ## Edit Tv
    from controllers.TvControllers import edit_tv

    @app.route("/tv/edit/<id>", methods=["POST"])
    def edit_tv_route(id):
        return edit_tv(id)

    ## Update view Tv
    from controllers.TvControllers import update_view_tv

    @app.route("/tv/updateview/<id>", methods=["POST"])
    def update_view_tv_route(id):
        return update_view_tv(id)
