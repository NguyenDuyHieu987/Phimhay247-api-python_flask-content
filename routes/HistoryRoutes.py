from flask import *

# from flask_cors import cross_origin
import configs
from controllers.HistoryControllers import History


def history_routes(app, cache):
    history = History()
    ## Get history

    @app.route("/history/get-all/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getall_history_route(type):
        return history.getall_history(type)

    ## Search history

    @app.route("/history/search/<type>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_history_route(type):
        return history.search_history(type)

    ## Get item history

    @app.route("/history/get/<type>/<movieId>", methods=["GET"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def get_history_route(type, movieId):
        return history.get_history(type, movieId)

    ## Add item to history

    @app.route("/history/add", methods=["POST"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def add_history_route():
        return history.add_history()

    ## Remove item from history

    @app.route("/history/remove", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_history_route():
        return history.remove_history()

    ## Remove all item from history

    @app.route("/history/clear", methods=["DELETE"])
    # @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def clear_history_route():
        return history.clear_history()
