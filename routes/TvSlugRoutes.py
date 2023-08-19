from flask import *
from flask_cors import cross_origin
import configs
from controllers.TvSlugControllers import TVSlug


def tv_slug_routes(app, cache):
    tvslug = TVSlug()

    @app.route("/tv/<slug>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached(query_string=True)
    def tv_slug_route(slug):
        return tvslug.tv_slug(slug)
