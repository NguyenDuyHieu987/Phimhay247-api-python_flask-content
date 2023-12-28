from flask import *

# from flask_cors import cross_origin
import configs
from controllers.TvControllers import TV


def tv_routes(app, cache):
    prefix_route = "tv"

    tv = TV()
    ## Detail Tv

    @app.route(f"/{prefix_route}/detail/<id>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    # @cache.cached()
    def get_tv_route(id):
        return tv.get(id)

    ## Add Tv

    @app.route(f"/{prefix_route}/add", methods=["POST"])
    # @cross_origin(origins=configs.API_ADMIN_ORIGINS_CONFIG)
    def add_tv_route():
        return tv.add()

    ## Edit Tv

    @app.route(f"/{prefix_route}/edit/<id>", methods=["POST"])
    # @cross_origin(origins=configs.API_ADMIN_ORIGINS_CONFIG)
    def edit_tv_route(id):
        return tv.edit(id)

    ## Update view Tv

    @app.route(f"/{prefix_route}/updateview/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def update_view_tv_route(id):
        return tv.update_view(id)
