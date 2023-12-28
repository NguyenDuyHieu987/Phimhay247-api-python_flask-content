from flask import *

# from flask_cors import cross_origin
import configs
from controllers.CreditsController import Credits


def credits_routes(app, cache):
    prefix_route = "credits"

    credits = Credits()

    @app.route(f"/{prefix_route}/<id>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_credits_route(id):
        return credits.get(id)
