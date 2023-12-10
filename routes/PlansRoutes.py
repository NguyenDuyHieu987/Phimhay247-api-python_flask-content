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

    @app.route("/plan/register/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def plans_register_route(id):
        return plan.register(id)

    @app.route("/plan/<method>/retrieve/<id>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def plans_retrieve_route(method, id):
        return plan.retrieve(method, id)
