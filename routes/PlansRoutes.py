from flask import *

# from flask_cors import cross_origin
import configs
from controllers.PlansControllers import Plan


def plans_routes(app, cache):
    prefix_route = "plan"

    plan = Plan()

    @app.route(f"/{prefix_route}/get-all", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    @cache.cached()
    def get_all_plans_route():
        return plan.get_all()

    @app.route(f"/{prefix_route}/register/<id>", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def register_plans_register_route(id):
        return plan.register(id)

    @app.route(f"/{prefix_route}/<method>/retrieve/<id>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def retrieve_plans_route(method, id):
        return plan.retrieve(method, id)
