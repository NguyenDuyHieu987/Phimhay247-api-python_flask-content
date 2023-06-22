from flask import *
from flask_cors import cross_origin
import configs
from controllers.CreditsController import Credits


def credits_routes(app, cache):
    credits = Credits()

    @app.route("/credits/<id>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def credits_route(id):
        return credits.get_credits(id)
