from flask import *

# from flask_cors import cross_origin
import configs
from controllers.TvSlugControllers import TVSlug


def tv_slug_routes(app, cache):
    prefix_route = "tv"

    tvslug = TVSlug()

    @app.route(f"/{prefix_route}/<slug>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached(query_string=True)
    def get_tv_slug_route(slug):
        return tvslug.get_slug(slug)

    @app.route(f"/{prefix_route}/discover/<slug>", methods=["GET"])
    @cache.cached(query_string=True)
    def filter_tv_slug_route(slug):
        return tvslug.filter(slug)
