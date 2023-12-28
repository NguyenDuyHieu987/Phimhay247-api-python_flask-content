from flask import *

# from flask_cors import cross_origin
import configs
from controllers.HistoryControllers import History


def history_routes(app, cache):
    prefix_route = "history"

    history = History()
    ## Get history

    @app.route(f"/{prefix_route}/get-all/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getall_history_route(type):
        return history.get_all(type)

    ## Search history

    @app.route(f"/{prefix_route}/search/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_history_route(type):
        return history.search(type)

    ## Get item history

    @app.route(f"/{prefix_route}/get/<type>/<movieId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_history_route(type, movieId):
        return history.get(type, movieId)

    ## Add item to history

    @app.route(f"/{prefix_route}/add", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def add_history_route():
        return history.add()

    ## Remove item from history

    @app.route(f"/{prefix_route}/remove", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_history_route():
        return history.remove()

    ## Remove all item from history

    @app.route(f"/{prefix_route}/clear", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def clear_history_route():
        return history.clear()
