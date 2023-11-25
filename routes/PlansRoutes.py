from flask import *
# from flask_cors import cross_origin
import configs
from controllers.PlansControllers import Plan


def plans_routes(app, cache):
    plan = Plan()

    @app.route("/plan/get", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def plans_route():
        return plan.plans()
