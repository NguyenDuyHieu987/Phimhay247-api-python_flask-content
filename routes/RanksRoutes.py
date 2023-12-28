from flask import *

# from flask_cors import cross_origin
import configs
from controllers.RanksControllers import Rank


def ranks_routes(app, cache):
    prefix_route = "ranks"

    rank = Rank()

    @app.route(f"/{prefix_route}/<slug>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_slug_ranks_route(slug):
        return rank.get_slug(slug)
