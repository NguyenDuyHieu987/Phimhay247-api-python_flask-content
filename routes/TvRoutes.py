from flask import *
from flask_cors import cross_origin
import configs
from controllers.TvControllers import TV


def tv_routes(app, cache):
    tv = TV()
    ## Detail Tv

    @cache.cached(timeout=3000)
    @app.route("/tv/detail/<id>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def detail_tv_route(id):
        return tv.detail_tv(id)

    ## Add Tv

    @app.route("/tv/add", methods=["POST"])
    @cross_origin(origins=configs.API_ADMIN_ORIGINS_CONFIG)
    def add_tv_route():
        return tv.add_tv()

    ## Edit Tv

    @app.route("/tv/edit/<id>", methods=["POST"])
    @cross_origin(origins=configs.API_ADMIN_ORIGINS_CONFIG)
    def edit_tv_route(id):
        return tv.edit_tv(id)

    ## Update view Tv

    @app.route("/tv/updateview/<id>", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def update_view_tv_route(id):
        return tv.update_view_tv(id)
