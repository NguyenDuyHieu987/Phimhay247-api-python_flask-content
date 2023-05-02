from flask import *
from flask_cors import cross_origin
import configs


def tv_slug_routes(app, cache):
    from controllers.TvSlugControllers import tv_slug

    @cache.cached(timeout=3600)
    @app.route("/tv/<slug>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def tv_slug_route(slug):
        return tv_slug(slug)
