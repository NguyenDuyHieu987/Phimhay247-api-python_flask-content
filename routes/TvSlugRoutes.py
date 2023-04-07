from flask import *


def tv_slug_routes(app):
    from controllers.TvSlugControllers import tv_slug

    @app.route("/tv/<slug>", methods=["GET"])
    def tv_slug_route(slug):
        return tv_slug(slug)
