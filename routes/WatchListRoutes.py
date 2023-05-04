from flask import *
from flask_cors import cross_origin
import configs
from controllers.WatchListControllers import WatchList


def watchlist_routes(app, cache):
    watchlist = WatchList()
    ## Get history

    @cache.cached(timeout=3600)
    @app.route("/history/<idwatchlist>/gethistory", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getwatchlist_route(idwatchlist):
        return watchlist.getwatchlist(idwatchlist)

    ## Search history

    @cache.cached(timeout=3600)
    @app.route("/history/<idwatchlist>/searchhistory", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def search_watchlist_route(idwatchlist):
        return watchlist.search_watchlist(idwatchlist)

    ## Get item history

    @cache.cached(timeout=3600)
    @app.route("/history/<idwatchlist>/getitem/<idmovie>", methods=["GET"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def getitem_watchlist_route(idwatchlist, idmovie):
        return watchlist.getitem_watchlist(idwatchlist, idmovie)

    ## Add item to history

    @app.route("/history/<idwatchlist>/add_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def additem_watchlist_route(idwatchlist):
        return watchlist.additem_watchlist(idwatchlist)

    ## Remove item from history

    @app.route("/history/<idwatchlist>/remove_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def remove_item_watchlist_route(idwatchlist):
        return watchlist.remove_item_watchlist(idwatchlist)

    ## Remove all item from history

    @app.route("/history/<idwatchlist>/removeall_item", methods=["POST"])
    @cross_origin(origins=configs.ALL_ORIGINS_CONFIG)
    def removeall_item_watchlist_route(idwatchlist):
        return watchlist.removeall_item_watchlist(idwatchlist)
