from flask import *
from flask_cors import cross_origin
import configs
from controllers.HistoryControllers import History


def history_routes(app, cache):
    history = History()
    ## Get history

    @app.route("/history/gethistory/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def gethistory_route(type):
        return history.gethistory(type)

    ## Search history

    @app.route("/history/searchhistory/<type>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_history_route(type):
        return history.search_history(type)

    ## Get item history

    @app.route("/history/getitem/<type>/<movieId>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getitem_history_route(type, movieId):
        return history.getitem_history(type, movieId)

    ## Add item to history

    @app.route("/history/add_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def additem_history_route():
        return history.additem_history()

    ## Remove item from history

    @app.route("/history/remove_item", methods=["DELETE"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_item_history_route():
        return history.remove_item_history()

    ## Remove all item from history

    @app.route("/history/removeall_item", methods=["DELETE"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def removeall_item_history_route():
        return history.removeall_item_history()
