from flask import *
from flask_cors import cross_origin
import configs
from controllers.WatchListControllers import WatchList


def watchlist_routes(app, cache):
    watchlist = WatchList()
    ## Get history

    @app.route("/history/gethistory", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getwatchlist_route():
        return watchlist.getwatchlist()

    ## Search history

    @app.route("/history/searchhistory", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_watchlist_route():
        return watchlist.search_watchlist()

    ## Get item history

    @app.route("/history/getitem/<idmovie>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getitem_watchlist_route(idmovie):
        return watchlist.getitem_watchlist(idmovie)

    ## Add item to history

    @app.route("/history/add_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def additem_watchlist_route():
        return watchlist.additem_watchlist()

    ## Remove item from history

    @app.route("/history/remove_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_item_watchlist_route():
        return watchlist.remove_item_watchlist()

    ## Remove all item from history

    @app.route("/history/removeall_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def removeall_item_watchlist_route():
        return watchlist.removeall_item_watchlist()
